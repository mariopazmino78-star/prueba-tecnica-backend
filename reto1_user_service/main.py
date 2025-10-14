from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import logging
from dotenv import load_dotenv

from config.database import connect_to_mongo, close_mongo_connection
from routes.user_routes import router as user_router

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
    logger.info("🚀 Starting User Service...")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("🛑 Shutting down User Service...")
    await close_mongo_connection()


# Crear aplicación FastAPI
app = FastAPI(
    title="User Service API",
    description="API REST para gestión de usuarios con FastAPI y MongoDB",
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
    Muestra método, ruta, tiempo de ejecución y código de estado.
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
app.include_router(user_router)


@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud para verificar que el servicio está activo"""
    return {
        "message": "User Service is running",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de health check para monitoreo"""
    return {
        "status": "healthy",
        "service": "user-service"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
