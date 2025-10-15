# Prueba Técnica – Backend Developer

Este proyecto contiene la solución completa para la prueba técnica de Backend Developer, implementando dos retos principales utilizando FastAPI, MongoDB y RabbitMQ.

## 🌐 Despliegue en Producción

**✅ TODOS LOS SERVICIOS DESPLEGADOS Y FUNCIONANDO**

### Reto 1 - User Service (CRUD)
- **URL:** https://prueba-tecnica-backend-production-61a8.up.railway.app
- **Swagger Docs:** https://prueba-tecnica-backend-production-61a8.up.railway.app/docs
- **Estado:** 🟢 Online

### Reto 2 - Orders Service (Microservicios)
- **URL:** https://tranquil-embrace-production.up.railway.app
- **Swagger Docs:** https://tranquil-embrace-production.up.railway.app/docs
- **Estado:** 🟢 Online

### Reto 2 - Notifications Service (Worker)
- **Tipo:** Background Worker
- **Estado:** 🟢 Listening for RabbitMQ messages

### Infraestructura Cloud
- **Railway:** Hosting de servicios Python
- **MongoDB Atlas:** Base de datos (M0 Free Tier)
- **CloudAMQP:** RabbitMQ como servicio (Little Lemur Free)

---

## 📦 Stack Tecnológico

- **Python 3.11**
- **FastAPI** - Framework web moderno y rápido
- **Motor** - Driver asíncrono de MongoDB
- **Pydantic v2** - Validación de datos
- **bcrypt** - Encriptación de contraseñas
- **pika** - Cliente de RabbitMQ
- **uvicorn** - Servidor ASGI

## 🏗️ Estructura del Proyecto

```
prueba-tecnica-backend/
├── README.md
├── .gitignore
│
├── reto1_user_service/          # RETO 1: CRUD de Usuarios
│   ├── main.py
│   ├── models/
│   │   └── user.py
│   ├── routes/
│   │   └── user_routes.py
│   ├── config/
│   │   └── database.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── docker-compose.yml
│   └── README.md
│
└── reto2_microservices/         # RETO 2: Microservicios
    ├── orders_service/
    │   ├── main.py
    │   ├── models/
    │   │   └── order.py
    │   ├── routes/
    │   │   └── orders.py
    │   ├── config/
    │   │   ├── database.py
    │   │   └── rabbit.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── notifications_service/
    │   ├── consumer.py
    │   ├── config/
    │   │   └── rabbit.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── docker-compose.yml
    ├── .env.example.local
    ├── .env.example.railway
    └── README.md
```

## 🎯 Reto 1: CRUD de Usuarios

API REST completa con operaciones CRUD sobre usuarios, utilizando FastAPI y MongoDB.

### Características:
- ✅ Endpoints: POST, GET, PUT, DELETE para usuarios
- ✅ Encriptación de contraseñas con bcrypt
- ✅ Validaciones con Pydantic
- ✅ Middleware para medir tiempo de respuesta
- ✅ MongoDB asíncrono con Motor
- ✅ Documentación automática en `/docs`

[Ver documentación completa →](./reto1_user_service/README.md)

## 🎯 Reto 2: Microservicios con RabbitMQ

Arquitectura de microservicios con comunicación asíncrona mediante colas de mensajería.

### Componentes:
- **Orders Service**: API para crear pedidos
- **Notifications Service**: Consumer que escucha y procesa pedidos

### Características:
- ✅ Comunicación desacoplada con RabbitMQ
- ✅ Persistencia en MongoDB
- ✅ Manejo de errores robusto
- ✅ Logs detallados

[Ver documentación completa →](./reto2_microservices/README.md)

## 🚀 Inicio Rápido

### Opción 1: Ejecutar Reto 1 (User Service)

```bash
cd reto1_user_service
docker-compose up --build
```

Acceder a: http://localhost:8000/docs

### Opción 2: Ejecutar Reto 2 (Microservicios)

```bash
cd reto2_microservices
docker-compose up --build
```

Acceder a: http://localhost:8001/docs

## 🌐 Despliegue en Railway

Ambos retos están diseñados para funcionar tanto en local como en Railway sin cambios en el código.

### Variables de Entorno Requeridas:

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
