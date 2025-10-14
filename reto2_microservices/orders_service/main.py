from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import logging
from dotenv import load_dotenv

from config.database import connect_to_mongo, close_mongo_connection
from config.rabbit import get_rabbitmq_publisher
from routes.orders import router as orders_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    Se ejecuta al inicio y al cierre de la aplicación.
    """
    # Startup
    logger.info("🚀 Starting Orders Service...")
    await connect_to_mongo()
    
    # Conectar a RabbitMQ
    try:
        publisher = get_rabbitmq_publisher()
        publisher.connect()
    except Exception as e:
        logger.error(f"⚠️ Could not connect to RabbitMQ on startup: {e}")
        logger.warning("Service will start but messages won't be published until RabbitMQ is available")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Orders Service...")
    await close_mongo_connection()
    
    # Cerrar conexión RabbitMQ
    try:
        publisher = get_rabbitmq_publisher()
        publisher.close()
    except Exception as e:
        logger.error(f"Error closing RabbitMQ connection: {e}")


# Crear aplicación FastAPI
app = FastAPI(
    title="Orders Service API",
    description="Microservicio de órdenes con comunicación asíncrona via RabbitMQ",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para medir tiempo de respuesta
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware que registra el tiempo de respuesta de cada petición.
    """
    start_time = time.time()
    
    # Procesar la petición
    response = await call_next(request)
    
    # Calcular tiempo de ejecución
    process_time = (time.time() - start_time) * 1000  # Convertir a milisegundos
    
    # Logging detallado
    logger.info(
        f"📊 {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}ms"
    )
    
    # Agregar header con el tiempo de respuesta
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    
    return response


# Incluir rutas
app.include_router(orders_router)


@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud para verificar que el servicio está activo"""
    return {
        "message": "Orders Service is running",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de health check para monitoreo"""
    return {
        "status": "healthy",
        "service": "orders-service"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
