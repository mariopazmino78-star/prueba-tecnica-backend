import os
import pika
import json
import logging
import time

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    """Consumer que escucha mensajes de RabbitMQ"""
    
    def __init__(self):
        self.connection = None
        self.channel = None
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        
    def connect(self):
        """Establece conexión con RabbitMQ"""
        try:
            logger.info(f"Connecting to RabbitMQ...")
            
            # Crear conexión
            parameters = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declarar cola (idempotente)
            self.channel.queue_declare(queue='orders_queue', durable=True)
            
            # Configurar QoS - procesar un mensaje a la vez
            self.channel.basic_qos(prefetch_count=1)
            
            logger.info("✅ Successfully connected to RabbitMQ")
            
        except Exception as e:
            logger.error(f"❌ Could not connect to RabbitMQ: {e}")
            raise
    
    def callback(self, ch, method, properties, body):
        """
        Callback que se ejecuta cuando se recibe un mensaje.
        
        Procesa el mensaje de la orden y lo registra en consola.
        """
        try:
            # Decodificar mensaje
            message = json.loads(body.decode('utf-8'))
            order_id = message.get('_id', 'unknown')
            product_name = message.get('product_name', 'unknown')
            quantity = message.get('quantity', 0)
            customer_email = message.get('customer_email', 'unknown')
            
            # LOG PRINCIPAL - Mostrar notificación de orden recibida
            logger.info(f"📧 New order received: {order_id}")
            logger.info(f"   Product: {product_name}")
            logger.info(f"   Quantity: {quantity}")
            logger.info(f"   Customer: {customer_email}")
            
            # Aquí se podría implementar lógica adicional:
            # - Enviar email al cliente
            # - Enviar notificación push
            # - Actualizar sistema de inventario
            # - etc.
            
            # Simular procesamiento
            time.sleep(0.5)
            
            # Confirmar que el mensaje fue procesado (ACK)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"✅ Order {order_id} processed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            # Rechazar mensaje y no re-encolar (evitar bucle infinito)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start_consuming(self):
        """Inicia el consumer para escuchar mensajes"""
        try:
            logger.info("👂 Starting to listen for orders...")
            logger.info("Waiting for messages. To exit press CTRL+C")
            
            # Configurar consumer
            self.channel.basic_consume(
                queue='orders_queue',
                on_message_callback=self.callback,
                auto_ack=False  # Manual ACK para mayor control
            )
            
            # Iniciar consumo (bloquea el hilo)
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("\n🛑 Consumer stopped by user")
            self.stop()
        except Exception as e:
            logger.error(f"❌ Error consuming messages: {e}")
            raise
    
    def stop(self):
        """Detiene el consumer y cierra la conexión"""
        try:
            if self.channel:
                self.channel.stop_consuming()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("✅ RabbitMQ connection closed")
        except Exception as e:
            logger.error(f"❌ Error closing connection: {e}")


def get_rabbitmq_consumer() -> RabbitMQConsumer:
    """Crea y retorna una instancia del consumer"""
    return RabbitMQConsumer()
