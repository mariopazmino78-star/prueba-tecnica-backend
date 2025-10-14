import os
import pika
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    """Publisher para enviar mensajes a RabbitMQ"""
    
    def __init__(self):
        self.connection = None
        self.channel = None
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        
    def connect(self):
        """Establece conexión con RabbitMQ"""
        try:
            # Parsear URL de RabbitMQ
            # Local: amqp://guest:guest@rabbitmq:5672/
            # CloudAMQP: amqps://user:pass@host/vhost
            logger.info(f"Connecting to RabbitMQ...")
            
            # Crear conexión
            parameters = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declarar cola (idempotente - si existe no hace nada)
            self.channel.queue_declare(queue='orders_queue', durable=True)
            
            logger.info("✅ Successfully connected to RabbitMQ")
            
        except Exception as e:
            logger.error(f"❌ Could not connect to RabbitMQ: {e}")
            raise
    
    def publish_order(self, order_data: Dict[str, Any]):
        """
        Publica un mensaje de orden en la cola 'orders_queue'
        
        Args:
            order_data: Diccionario con los datos de la orden
        """
        try:
            if not self.channel:
                self.connect()
            
            # Convertir a JSON
            message = json.dumps(order_data, default=str)
            
            # Publicar mensaje
            self.channel.basic_publish(
                exchange='',
                routing_key='orders_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Hacer mensaje persistente
                    content_type='application/json'
                )
            )
            
            logger.info(f"✅ Published order to queue: {order_data.get('_id')}")
            
        except Exception as e:
            logger.error(f"❌ Error publishing to RabbitMQ: {e}")
            # Intentar reconectar
            try:
                self.close()
                self.connect()
                # Reintentar publicación
                message = json.dumps(order_data, default=str)
                self.channel.basic_publish(
                    exchange='',
                    routing_key='orders_queue',
                    body=message,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        content_type='application/json'
                    )
                )
                logger.info(f"✅ Published order to queue (retry): {order_data.get('_id')}")
            except Exception as retry_error:
                logger.error(f"❌ Error on retry: {retry_error}")
                raise
    
    def close(self):
        """Cierra la conexión con RabbitMQ"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("✅ RabbitMQ connection closed")
        except Exception as e:
            logger.error(f"❌ Error closing RabbitMQ connection: {e}")


# Instancia global del publisher
rabbitmq_publisher = RabbitMQPublisher()


def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """Retorna la instancia global del publisher"""
    return rabbitmq_publisher
