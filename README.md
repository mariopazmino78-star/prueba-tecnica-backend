# Prueba Técnica – Backend Developer

Solución completa de prueba técnica implementando CRUD de usuarios y arquitectura de microservicios con FastAPI, MongoDB y RabbitMQ.

---

## 🌐 Servicios en Producción

### 🔹 Reto 1 - User Service (CRUD)
**API REST con operaciones CRUD completas para gestión de usuarios**

- **URL Base:** https://prueba-tecnica-backend-production-61a8.up.railway.app
- **Documentación:** https://prueba-tecnica-backend-production-61a8.up.railway.app/docs
- **Estado:** 🟢 Online

**Funcionalidades:**
- Crear usuarios con validación de datos
- Listar todos los usuarios
- Obtener usuario por ID
- Actualizar información de usuarios
- Eliminar usuarios
- Encriptación de contraseñas con bcrypt

---

### 🔹 Reto 2 - Microservicios con RabbitMQ

#### Orders Service (API)
**API REST para gestión de órdenes con mensajería asíncrona**

- **URL Base:** https://tranquil-embrace-production.up.railway.app
- **Documentación:** https://tranquil-embrace-production.up.railway.app/docs
- **Estado:** 🟢 Online

**Funcionalidades:**
- Crear órdenes de productos
- Consultar órdenes por ID
- Envío automático de notificaciones vía RabbitMQ

#### Notifications Service (Worker)
**Servicio de procesamiento de notificaciones en segundo plano**

- **Tipo:** Consumer de RabbitMQ
- **Estado:** 🟢 Escuchando mensajes

**Funcionalidades:**
- Recibe mensajes de la cola `orders_queue`
- Procesa notificaciones de nuevas órdenes
- Logs detallados de cada notificación

---

## 🏗️ Infraestructura

| Componente | Servicio | Plan |
|------------|----------|------|
| **Hosting** | Railway | Developer ($5/mes) |
| **Base de Datos** | MongoDB Atlas | M0 Free Tier |
| **Message Broker** | CloudAMQP | Little Lemur Free |

---

## �️ Stack Tecnológico

- **Python 3.11** - Lenguaje de programación
- **FastAPI** - Framework web async
- **Motor** - Driver asíncrono de MongoDB
- **Pydantic v2** - Validación de datos
- **bcrypt** - Encriptación de contraseñas
- **pika** - Cliente de RabbitMQ
- **uvicorn** - Servidor ASGI

## 🏗️ Estructura del Proyecto

```
prueba-tecnica-backend/
├── README.md                    # Este archivo
├── reto1_user_service/          # Reto 1: CRUD de Usuarios
│   ├── config/                  # Configuración (DB)
│   ├── models/                  # Modelos Pydantic
│   ├── routes/                  # Endpoints API
│   ├── main.py                  # Aplicación FastAPI
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md                # Documentación detallada
│
└── reto2_microservices/         # Reto 2: Microservicios
    ├── orders_service/          # API de órdenes
    │   ├── config/              # DB y RabbitMQ
    │   ├── models/              # Modelos
    │   ├── routes/              # Endpoints
    │   └── main.py
    │
    ├── notifications_service/   # Consumer de notificaciones
    │   ├── config/              # RabbitMQ
    │   └── main.py
    │
    ├── docker-compose.yml
    └── README.md                # Documentación detallada
```

---

## 🚀 Ejecución Local

### Reto 1 - User Service

```bash
cd reto1_user_service
docker-compose up --build
```

**Acceder a:** http://localhost:8000/docs

### Reto 2 - Microservicios

```bash
cd reto2_microservices
docker-compose up --build
```

**Acceder a:** http://localhost:8002/docs

---

## 🧪 Pruebas

### Probar Reto 1 (CRUD Usuarios)

1. Ir a https://prueba-tecnica-backend-production-61a8.up.railway.app/docs
2. POST `/users/` - Crear usuario
3. GET `/users/` - Listar usuarios
4. GET `/users/{id}` - Obtener usuario
5. PUT `/users/{id}` - Actualizar usuario
6. DELETE `/users/{id}` - Eliminar usuario

### Probar Reto 2 (Microservicios)

1. Ir a https://tranquil-embrace-production.up.railway.app/docs
2. POST `/orders/` - Crear orden
3. Verificar logs del Notifications Service en Railway
4. Ver mensaje: "📧 New order received: {order_id}"

---

## 📚 Documentación Adicional

- **Reto 1:** Ver [reto1_user_service/README.md](./reto1_user_service/README.md)
- **Reto 2:** Ver [reto2_microservices/README.md](./reto2_microservices/README.md)

---

## 👨‍💻 Desarrollador

**Mario Pazmiño**  
**GitHub:** https://github.com/mariopazmino78-star/prueba-tecnica-backend  
**Fecha:** Octubre 2025

**Para servicios con MongoDB:**
- `MONGODB_URI` - Conexión a MongoDB Atlas

**Para servicios con RabbitMQ:**
- `RABBITMQ_URL` - Conexión a CloudAMQP

Ver archivos `.env.example.railway` en cada proyecto para configuración detallada.

## 📝 Documentación API

### Reto 1 - User Service
- **POST** `/users/` - Crear usuario
- **GET** `/users/{id}` - Obtener usuario
- **PUT** `/users/{id}` - Actualizar usuario
- **DELETE** `/users/{id}` - Eliminar usuario

### Reto 2 - Orders Service
- **POST** `/orders/` - Crear pedido (dispara notificación)

## 🧪 Pruebas

Cada reto incluye ejemplos de curl y colecciones de Postman en su respectivo README.

## 📄 Licencia

Proyecto de prueba técnica - 2025

## 👨‍💻 Autor

Mario Pazmiño
prueba-tecnica-backend
