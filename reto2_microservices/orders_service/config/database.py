import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database connection manager"""
    client: Optional[AsyncIOMotorClient] = None
    db = None

# Global database instance
database = Database()

async def connect_to_mongo():
    """
    Establece conexión con MongoDB usando la URI de las variables de entorno.
    Funciona tanto para MongoDB local como MongoDB Atlas (Railway).
    """
    try:
        # Obtener URI desde variables de entorno
        # Local: mongodb://mongodb:27017
        # Railway: mongodb+srv://user:pass@cluster.mongodb.net
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "orders_db")
        
        logger.info(f"Connecting to MongoDB at: {mongodb_uri.split('@')[-1] if '@' in mongodb_uri else mongodb_uri}")
        
        # Crear cliente de MongoDB asíncrono
        database.client = AsyncIOMotorClient(mongodb_uri)
        database.db = database.client[database_name]
        
        # Verificar conexión
        await database.client.admin.command('ping')
        logger.info(f"✅ Successfully connected to MongoDB database: {database_name}")
        
    except Exception as e:
        logger.error(f"❌ Could not connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Cierra la conexión con MongoDB"""
    try:
        if database.client:
            database.client.close()
            logger.info("✅ MongoDB connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing MongoDB connection: {e}")

def get_database():
    """Retorna la instancia de la base de datos"""
    return database.db
