# Reto 2: Comunicación entre Microservicios (RabbitMQ)

## � Despliegue en Producción

**✅ DESPLEGADO EXITOSAMENTE EN RAILWAY + CLOUDAMQP**

### Orders Service (API REST)
- **URL API:** https://tranquil-embrace-production.up.railway.app
- **Documentación Swagger:** https://tranquil-embrace-production.up.railway.app/docs
- **Health Check:** https://tranquil-embrace-production.up.railway.app/health
- **Base de Datos:** MongoDB Atlas (orders_db)
- **Message Broker:** CloudAMQP (RabbitMQ Free Tier)
- **Estado:** 🟢 Online y Funcionando

### Notifications Service (Worker)
- **Tipo:** Background Worker (Consumer)
- **Message Broker:** CloudAMQP (RabbitMQ Free Tier)
- **Estado:** 🟢 Listening for messages
- **Logs:** Visible en Railway Dashboard

## �🎯 Objetivo

Evaluar el diseño de microservicios desacoplados con colas de mensajería mediante RabbitMQ.

## 📋 Funcionalidad Implementada

### 1. Dos Microservicios:
- ✅ **orders_service** → Crea pedidos y publica mensajes
- ✅ **notifications_service** → Escucha mensajes de RabbitMQ

### 2. Flujo POST /orders:
- ✅ Guarda el pedido en MongoDB
- ✅ Publica un mensaje en la cola `orders_queue`

### 3. Notifications Service:
- ✅ Escucha la cola y muestra en consola: **"New order received: {order_id}"**

---

## �️ Arquitectura

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

---

## 📦 Componentes

### 1. Orders Service
- **Puerto**: 8002
- **Función**: API REST para crear y consultar órdenes
- **Stack**: FastAPI + Motor (MongoDB) + pika (RabbitMQ)
- **Endpoints**:
  - `POST /orders/` - Crear orden y publicar a RabbitMQ
  - `GET /orders/{id}` - Consultar orden por ID

### 2. Notifications Service
- **Función**: Consumer que escucha mensajes de RabbitMQ
- **Stack**: Python + pika
- **Proceso**: Recibe mensajes de nuevas órdenes y muestra en consola

### 3. RabbitMQ
- **Puerto AMQP**: 5672
- **Puerto Management UI**: 15672
- **Cola**: `orders_queue`
- **Credenciales**: guest/guest (local)

### 4. MongoDB
- **Puerto Local**: 27018 (para evitar conflicto con Reto 1)
- **Puerto Interno Container**: 27017
- **Base de datos**: `orders_db`
- **Colección**: `orders`

---

## 🚀 Cómo Levantar en Local

### Opción 1: Docker Compose (Recomendado)

Este comando levanta **todos los servicios** incluyendo RabbitMQ:

```bash
# Navegar al directorio
cd reto2_microservices

# Levantar todos los servicios (MongoDB, RabbitMQ, Orders Service, Notifications Service)
docker-compose up --build

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo del servicio de notificaciones
docker-compose logs -f notifications_service
```

**Servicios disponibles:**
- 📦 **Orders API**: http://localhost:8002
- 📖 **Swagger Docs**: http://localhost:8002/docs
- 🐰 **RabbitMQ Management**: http://localhost:15672 (usuario: `guest`, password: `guest`)

**Puertos utilizados:**
- `8002` - Orders Service API
- `27018` - MongoDB (externo, para evitar conflicto con Reto 1)
- `5672` - RabbitMQ AMQP
- `15672` - RabbitMQ Management UI

---

## 🧪 Cómo Probar el Flujo Completo

### Paso 1: Crear un Pedido (POST /orders)

**Con PowerShell:**
```powershell
$body = @{
    product_name = "Laptop Dell XPS 15"
    quantity = 3
    customer_email = "cliente@example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8002/orders/" -Method Post -ContentType "application/json" -Body $body
```

**Con curl:**
```bash
curl -X POST "http://localhost:8002/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop Dell XPS 15",
    "quantity": 3,
    "customer_email": "cliente@example.com"
  }'
```

**Respuesta esperada (201 Created):**
```json
{
  "_id": "68eeed726df17fded69dd236",
  "product_name": "Laptop Dell XPS 15",
  "quantity": 3,
  "customer_email": "cliente@example.com",
  "created_at": "2025-10-15T00:40:18.209000",
  "status": "pending"
}
```

### Paso 2: Ver la Notificación en Consola

En los logs del `notifications_service` verás **exactamente esto**:

```
notifications_service | 📧 New order received: 68eeed726df17fded69dd236
notifications_service |    Product: Laptop Dell XPS 15
notifications_service |    Quantity: 3
notifications_service |    Customer: cliente@example.com
notifications_service | ✅ Order 68eeed726df17fded69dd236 processed successfully
```

✅ **Cumple con el requisito**: `"New order received: {order_id}"`

### Paso 3: Verificar que se Guardó en MongoDB

**Consultar la orden creada:**
```bash
curl -X GET "http://localhost:8002/orders/68eeed726df17fded69dd236"
```

**O usar Swagger Docs:**
1. Ir a http://localhost:8002/docs
2. Expandir `GET /orders/{order_id}`
3. Click en "Try it out"
4. Pegar el ID de la orden
5. Click en "Execute"

---

## 📁 Entregables (100% Completo)

### ✅ Carpeta `/orders_service/`
- ✅ `main.py` - Aplicación FastAPI con lifespan
- ✅ `routes/orders.py` - Endpoint POST /orders
- ✅ `config/rabbit.py` - Publicador RabbitMQ
- ✅ `Dockerfile` - Imagen Docker
- **Extras**: `models/order.py`, `config/database.py`, `requirements.txt`

### ✅ Carpeta `/notifications_service/`
- ✅ `consumer.py` - Consumidor principal
- ✅ `config/rabbit.py` - Consumer RabbitMQ
- ✅ `Dockerfile` - Imagen Docker
- **Extras**: `requirements.txt`

### ✅ Carpeta raíz `/reto2_microservices/`
- ✅ `docker-compose.yml` - Orquesta todos los servicios (MongoDB, RabbitMQ, ambos microservicios)
- ✅ `.env.example.local` - Variables para desarrollo local (MONGODB_URI, RABBITMQ_URL)
- ✅ `.env.example.railway` - Variables para Railway
- ✅ `README.md` - Este archivo con instrucciones completas

---

## 📊 Verificación de Requisitos

| Requisito | Estado | Evidencia |
|-----------|--------|-----------|
| **POST /orders guarda en MongoDB** | ✅ | `routes/orders.py` línea 38-41 |
| **POST /orders publica a RabbitMQ** | ✅ | `routes/orders.py` línea 48-57 |
| **Muestra "New order received: {order_id}"** | ✅ | `config/rabbit.py` línea 51-54 |
| **Integración correcta RabbitMQ** | ✅ | Cola `orders_queue`, mensajes persistentes |
| **Diseño asíncrono** | ✅ | Motor (async), FastAPI async |
| **Manejo de errores** | ✅ | Try/except, retries, logs detallados |
| **Claridad de logs** | ✅ | Emojis, información estructurada |

---

## 🌐 Despliegue en Railway (Servicios Independientes)

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

**Nota**: Railway asignará automáticamente un puerto y URL pública.

#### 2. Desplegar Notifications Service

```bash
# En Railway, crear nuevo servicio desde GitHub
# Configurar directorio raíz: reto2_microservices/notifications_service

# Variable de entorno:
RABBITMQ_URL=amqps://user:pass@host.cloudamqp.com/vhost
```

**Nota**: Este servicio NO necesita puerto público, solo escucha RabbitMQ.

#### 3. Verificar Despliegue

```bash
# Probar Orders Service (usar la URL que Railway te asigna)
curl -X POST "https://tu-orders-service.railway.app/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "quantity": 1,
    "customer_email": "test@example.com"
  }'

# Verificar logs de Notifications Service en Railway Dashboard
# Deberías ver: "📧 New order received: {order_id}"
```

---

## 🧪 Pruebas Adicionales

### Con PowerShell (Recomendado para Windows)

```powershell
# Test 1: Crear orden
$body = @{
    product_name = "iPhone 15 Pro"
    quantity = 2
    customer_email = "cliente@test.com"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8002/orders/" -Method Post -ContentType "application/json" -Body $body
Write-Host "Orden creada con ID: $($response._id)" -ForegroundColor Green

# Test 2: Consultar orden
Invoke-RestMethod -Uri "http://localhost:8002/orders/$($response._id)" -Method Get
```

### Con Swagger UI

1. Abrir http://localhost:8002/docs
2. Expandir `POST /orders/`
3. Click en "Try it out"
4. Ingresar datos de prueba
5. Click en "Execute"
6. Ver respuesta y logs del notifications_service

---

## 📊 Monitoreo y Características Técnicas

### RabbitMQ Management UI (Local)

Acceder a: http://localhost:15672
- Usuario: `guest`
- Contraseña: `guest`

Funcionalidades:
- ✅ Ver mensajes en la cola `orders_queue`
- ✅ Monitorear conexiones activas
- ✅ Estadísticas de throughput
- ✅ Gestionar exchanges y bindings

### Manejo de Errores y Resiliencia

**Orders Service:**
- ✅ Validación de datos con Pydantic (quantity > 0, email válido)
- ✅ Manejo de errores de MongoDB con try/except
- ✅ Si RabbitMQ falla, la orden se guarda igual
- ✅ Logs detallados de cada operación

**Notifications Service:**
- ✅ Reconexión automática a RabbitMQ (5 reintentos con delay de 5s)
- ✅ Manual ACK para garantizar procesamiento correcto
- ✅ NACK en caso de error (sin requeue para evitar bucles)
- ✅ Logs claros con emojis para fácil identificación

### Logging Estructurado

Formato: `TIMESTAMP - SERVICE - LEVEL - MESSAGE`

**Ejemplo de flujo completo:**
```
orders_service     | 📊 POST /orders/ - Status: 201 - Time: 45.32ms
orders_service     | ✅ Order created in database: 68eeed726df17fded69dd236
orders_service     | ✅ Order published to RabbitMQ: 68eeed726df17fded69dd236
notifications      | 📧 New order received: 68eeed726df17fded69dd236
notifications      |    Product: Laptop Dell XPS 15
notifications      |    Quantity: 3
notifications      |    Customer: cliente@example.com
notifications      | ✅ Order 68eeed726df17fded69dd236 processed successfully
```

---

## 📝 Resumen de Puertos

### Desarrollo Local (ambos Retos corriendo simultáneamente)

| Servicio | Puerto | Uso |
|----------|--------|-----|
| **Reto 1 - User Service** | 8000 | API CRUD usuarios |
| **Reto 1 - MongoDB** | 27017 | Base de datos usuarios |
| **Reto 2 - Orders Service** | 8002 | API órdenes |
| **Reto 2 - MongoDB** | 27018 | Base de datos órdenes |
| **Reto 2 - RabbitMQ AMQP** | 5672 | Broker mensajes |
| **Reto 2 - RabbitMQ UI** | 15672 | Interfaz web |

---

## 🎯 Evaluación - Criterios Cumplidos

| Criterio | Estado | Evidencia |
|----------|--------|-----------|
| **Correcta integración con RabbitMQ** | ✅ | Cola declarada, mensajes persistentes, ACK manual |
| **Diseño asíncrono** | ✅ | Motor async, FastAPI async, endpoints con async/await |
| **Manejo de errores** | ✅ | Try/except en todas las operaciones críticas, retries |
| **Claridad de logs** | ✅ | Logs con emojis, información estructurada, timestamps |
| **Despliegue Railway** | ✅ | Instrucciones completas, variables de entorno documentadas |

---

## 📄 Licencia

Proyecto de prueba técnica - 2025

## 👨‍💻 Autor

Mario Pazmiño
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
