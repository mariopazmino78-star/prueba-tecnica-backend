# Reto 2: Microservicios con RabbitMQ

Arquitectura de microservicios con comunicación asíncrona utilizando RabbitMQ como message broker. Incluye un servicio de órdenes y un servicio de notificaciones.

## 🎯 Arquitectura

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────────┐
│  Orders Service │─────▶│   RabbitMQ   │─────▶│ Notifications       │
│   (FastAPI)     │      │ orders_queue │      │ Service (Consumer)  │
└─────────────────┘      └──────────────┘      └─────────────────────┘
         │                                                 │
         ▼                                                 ▼
   ┌──────────┐                                    ┌──────────┐
   │ MongoDB  │                                    │   Logs   │
   └──────────┘                                    └──────────┘
```

## 🏗️ Componentes

### 1. Orders Service
- **Puerto**: 8001
- **Función**: API REST para crear y consultar órdenes
- **Stack**: FastAPI + Motor (MongoDB) + pika (RabbitMQ)
- **Endpoints**:
  - `POST /orders/` - Crear orden y publicar a RabbitMQ
  - `GET /orders/{id}` - Consultar orden por ID

### 2. Notifications Service
- **Función**: Consumer que escucha mensajes de RabbitMQ
- **Stack**: Python + pika
- **Proceso**: Recibe mensajes de nuevas órdenes y los registra en consola

### 3. RabbitMQ
- **Puerto AMQP**: 5672
- **Puerto Management UI**: 15672
- **Cola**: `orders_queue`
- **Credenciales**: guest/guest (local)

### 4. MongoDB
- **Puerto**: 27017
- **Base de datos**: `orders_db`
- **Colección**: `orders`

## 🚀 Inicio Rápido

### Opción 1: Docker Compose (Recomendado)

```bash
# Navegar al directorio
cd reto2_microservices

# Levantar todos los servicios
docker-compose up --build

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo de notifications
docker-compose logs -f notifications_service
```

**Servicios disponibles:**
- Orders API: http://localhost:8001
- API Docs: http://localhost:8001/docs
- RabbitMQ Management: http://localhost:15672 (guest/guest)

### Opción 2: Manual (requiere MongoDB y RabbitMQ locales)

**Terminal 1 - Orders Service:**
```bash
cd orders_service
pip install -r requirements.txt
export MONGODB_URI="mongodb://localhost:27017"
export DATABASE_NAME="orders_db"
export RABBITMQ_URL="amqp://guest:guest@localhost:5672/"
python main.py
```

**Terminal 2 - Notifications Service:**
```bash
cd notifications_service
pip install -r requirements.txt
export RABBITMQ_URL="amqp://guest:guest@localhost:5672/"
python consumer.py
```

## 📋 Flujo de Trabajo Completo

### 1. Crear una Orden

```bash
curl -X POST "http://localhost:8001/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop HP Pavilion",
    "quantity": 2,
    "customer_email": "customer@example.com"
  }'
```

**Respuesta (201 Created):**
```json
{
  "id": "65a1b2c3d4e5f6g7h8i9j0k1",
  "product_name": "Laptop HP Pavilion",
  "quantity": 2,
  "customer_email": "customer@example.com",
  "created_at": "2025-01-15T10:30:00.123Z",
  "status": "pending"
}
```

### 2. Ver la Notificación

En los logs del `notifications_service` verás:

```
2025-01-15 10:30:00 - __main__ - INFO - 📧 New order received: 65a1b2c3d4e5f6g7h8i9j0k1
2025-01-15 10:30:00 - __main__ - INFO -    Product: Laptop HP Pavilion
2025-01-15 10:30:00 - __main__ - INFO -    Quantity: 2
2025-01-15 10:30:00 - __main__ - INFO -    Customer: customer@example.com
2025-01-15 10:30:00 - __main__ - INFO - ✅ Order 65a1b2c3d4e5f6g7h8i9j0k1 processed successfully
```

### 3. Consultar la Orden

```bash
curl -X GET "http://localhost:8001/orders/65a1b2c3d4e5f6g7h8i9j0k1"
```

## 🌐 Despliegue en Railway

### Prerequisitos

1. **MongoDB Atlas** (gratis)
   - Crear cuenta: https://www.mongodb.com/cloud/atlas
   - Crear cluster M0 (gratis)
   - Network Access: permitir `0.0.0.0/0`
   - Obtener connection string

2. **CloudAMQP** (gratis)
   - Crear cuenta: https://www.cloudamqp.com
   - Crear instancia "Little Lemur" (gratis)
   - Copiar AMQP URL

### Pasos de Despliegue

#### 1. Desplegar Orders Service

```bash
# En Railway, crear nuevo servicio desde GitHub
# Configurar directorio raíz: reto2_microservices/orders_service

# Variables de entorno:
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/orders_db?retryWrites=true&w=majority
DATABASE_NAME=orders_db
RABBITMQ_URL=amqps://user:pass@host.cloudamqp.com/vhost
```

#### 2. Desplegar Notifications Service

```bash
# En Railway, crear nuevo servicio desde GitHub
# Configurar directorio raíz: reto2_microservices/notifications_service

# Variable de entorno:
RABBITMQ_URL=amqps://user:pass@host.cloudamqp.com/vhost
```

#### 3. Verificar Despliegue

```bash
# Probar Orders Service
curl -X POST "https://orders-service.railway.app/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "quantity": 1,
    "customer_email": "test@example.com"
  }'

# Verificar logs de Notifications Service en Railway Dashboard
```

## 🧪 Pruebas con Postman

### Colección Postman

```json
{
  "info": {
    "name": "Microservices API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Order",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"product_name\": \"iPhone 15 Pro\",\n  \"quantity\": 1,\n  \"customer_email\": \"john@example.com\"\n}"
        },
        "url": "{{base_url}}/orders/"
      }
    },
    {
      "name": "Get Order",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/orders/{{order_id}}"
      }
    }
  ]
}
```

**Variables:**
- `base_url`: `http://localhost:8001` (local) o tu URL de Railway

## 📊 Monitoreo

### RabbitMQ Management UI (Local)

Acceder a: http://localhost:15672
- Usuario: `guest`
- Contraseña: `guest`

Desde aquí puedes:
- Ver mensajes en la cola
- Monitorear conexiones
- Ver estadísticas de throughput
- Gestionar exchanges y bindings

### CloudAMQP Dashboard (Railway)

Acceder desde tu panel de CloudAMQP:
- Ver mensajes en tránsito
- Monitorear conexiones activas
- Ver gráficos de rendimiento
- Configurar alertas

## 🔧 Características Técnicas

### Manejo de Errores

**Orders Service:**
- Validación de datos con Pydantic
- Manejo de errores de MongoDB
- Retry logic para RabbitMQ
- Logs detallados de errores

**Notifications Service:**
- Reconexión automática a RabbitMQ
- Manual ACK para garantizar procesamiento
- NACK en caso de error (sin requeue)
- Reintentos con backoff

### Resiliencia

- **Health Checks**: Endpoints `/health` en Orders Service
- **Restart Policies**: `on-failure` en docker-compose
- **Connection Pooling**: Gestión eficiente de conexiones
- **Graceful Shutdown**: Cierre ordenado de conexiones

### Logging

Todos los servicios incluyen logging estructurado:
```
TIMESTAMP - SERVICE - LEVEL - MESSAGE
```

Ejemplos:
```
2025-01-15 10:30:00 - orders_service - INFO - ✅ Order created in database: 65a1b...
2025-01-15 10:30:00 - orders_service - INFO - ✅ Order published to RabbitMQ: 65a1b...
2025-01-15 10:30:01 - notifications - INFO - 📧 New order received: 65a1b...
```

## 📝 Variables de Entorno

| Variable | Servicio | Descripción | Local | Railway |
|----------|----------|-------------|-------|---------|
| `MONGODB_URI` | Orders | URI de MongoDB | `mongodb://mongodb:27017` | `mongodb+srv://...` |
| `DATABASE_NAME` | Orders | Nombre de BD | `orders_db` | `orders_db` |
| `RABBITMQ_URL` | Ambos | URL de RabbitMQ | `amqp://guest:guest@rabbitmq:5672/` | `amqps://...` |

## 🐛 Troubleshooting

### RabbitMQ no conecta

```bash
# Verificar que RabbitMQ esté corriendo
docker-compose ps rabbitmq

# Ver logs de RabbitMQ
docker-compose logs rabbitmq

# Verificar health check
docker-compose ps
```

### Notifications no recibe mensajes

```bash
# Ver logs del consumer
docker-compose logs -f notifications_service

# Verificar cola en RabbitMQ Management UI
# http://localhost:15672 → Queues → orders_queue

# Reiniciar el servicio
docker-compose restart notifications_service
```

### MongoDB no conecta

```bash
# Verificar MongoDB
docker-compose logs mongodb

# Verificar variables de entorno
docker-compose exec orders_service env | grep MONGODB
```

### Reiniciar todo

```bash
# Detener y eliminar todo
docker-compose down -v

# Volver a levantar
docker-compose up --build
```

## 🎓 Conceptos Implementados

- ✅ **Microservicios**: Servicios independientes y desacoplados
- ✅ **Message Queue**: Comunicación asíncrona con RabbitMQ
- ✅ **Publisher-Subscriber**: Patrón de mensajería
- ✅ **Event-Driven**: Arquitectura basada en eventos
- ✅ **Async/Await**: Operaciones asíncronas en Python
- ✅ **Docker Compose**: Orquestación de múltiples servicios
- ✅ **Health Checks**: Monitoreo de servicios
- ✅ **Graceful Degradation**: Manejo de fallos

## 📄 Licencia

Proyecto de prueba técnica - 2025

## 👨‍💻 Autor

Mario Pazmiño
