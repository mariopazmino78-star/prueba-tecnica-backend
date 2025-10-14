from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import logging

from models.order import OrderCreate, OrderResponse
from config.database import get_database
from config.rabbit import get_rabbitmq_publisher

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """
    Crear una nueva orden.
    
    - **product_name**: Nombre del producto
    - **quantity**: Cantidad de productos (debe ser > 0)
    - **customer_email**: Email del cliente
    
    Este endpoint:
    1. Guarda la orden en MongoDB
    2. Publica un mensaje en RabbitMQ (cola: orders_queue)
    3. El servicio de notificaciones escuchará y procesará el mensaje
    """
    try:
        db = get_database()
        
        # Crear documento de orden
        order_dict = {
            "product_name": order.product_name,
            "quantity": order.quantity,
            "customer_email": order.customer_email,
            "created_at": datetime.utcnow(),
            "status": "pending"
        }
        
        # Guardar en MongoDB
        result = await db.orders.insert_one(order_dict)
        
        # Obtener la orden creada
        created_order = await db.orders.find_one({"_id": result.inserted_id})
        
        logger.info(f"✅ Order created in database: {result.inserted_id}")
        
        # Publicar mensaje en RabbitMQ
        try:
            publisher = get_rabbitmq_publisher()
            publisher.publish_order({
                "_id": str(created_order["_id"]),
                "product_name": created_order["product_name"],
                "quantity": created_order["quantity"],
                "customer_email": created_order["customer_email"],
                "created_at": created_order["created_at"],
                "status": created_order["status"]
            })
            logger.info(f"✅ Order published to RabbitMQ: {result.inserted_id}")
        except Exception as rabbit_error:
            # Loguear error pero no fallar la petición
            # La orden ya está guardada en la BD
            logger.error(f"⚠️ Error publishing to RabbitMQ: {rabbit_error}")
            logger.warning(f"Order {result.inserted_id} created but not published to queue")
        
        # Retornar respuesta
        return OrderResponse(
            _id=str(created_order["_id"]),
            product_name=created_order["product_name"],
            quantity=created_order["quantity"],
            customer_email=created_order["customer_email"],
            created_at=created_order["created_at"],
            status=created_order["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating order: {str(e)}"
        )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """
    Obtener una orden por su ID.
    
    - **order_id**: ID único de la orden (ObjectId de MongoDB)
    """
    try:
        from bson import ObjectId
        db = get_database()
        
        # Validar ObjectId
        if not ObjectId.is_valid(order_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order ID format"
            )
        
        # Buscar orden
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {order_id} not found"
            )
        
        logger.info(f"✅ Order retrieved: {order_id}")
        
        return OrderResponse(
            _id=str(order["_id"]),
            product_name=order["product_name"],
            quantity=order["quantity"],
            customer_email=order["customer_email"],
            created_at=order["created_at"],
            status=order.get("status", "pending")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error retrieving order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving order: {str(e)}"
        )
