import logging
import time
from dotenv import load_dotenv
from config.rabbit import get_rabbitmq_consumer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()


def main():
    """
    Función principal del servicio de notificaciones.
    
    Este servicio escucha la cola 'orders_queue' en RabbitMQ
    y procesa los mensajes de nuevas órdenes.
    """
    logger.info("🚀 Starting Notifications Service...")
    
    max_retries = 5
    retry_delay = 5  # segundos
    
    for attempt in range(1, max_retries + 1):
        try:
            # Crear consumer
            consumer = get_rabbitmq_consumer()
            
            # Conectar a RabbitMQ
            consumer.connect()
            
            # Iniciar consumo de mensajes (bloquea hasta CTRL+C)
            consumer.start_consuming()
            
            # Si llega aquí, fue detenido manualmente
            break
            
        except KeyboardInterrupt:
            logger.info("\n🛑 Service stopped by user")
            break
            
        except Exception as e:
            logger.error(f"❌ Error in notifications service (attempt {attempt}/{max_retries}): {e}")
            
            if attempt < max_retries:
                logger.info(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"❌ Max retries reached. Service shutting down.")
                raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        exit(1)
