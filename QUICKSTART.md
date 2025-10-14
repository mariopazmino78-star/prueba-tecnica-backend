# 🚀 Inicio Rápido - Prueba Técnica Backend

## ✅ Estructura Creada

```
prueba-tecnica-backend/
├── README.md ✅
├── .gitignore ✅
├── reto1_user_service/ ✅
│   ├── main.py
│   ├── models/user.py
│   ├── routes/user_routes.py
│   ├── config/database.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── docker-compose.yml
│   └── README.md
└── reto2_microservices/ ✅
    ├── orders_service/
    │   ├── main.py
    │   ├── models/order.py
    │   ├── routes/orders.py
    │   ├── config/database.py
    │   ├── config/rabbit.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── notifications_service/
    │   ├── consumer.py
    │   ├── config/rabbit.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── docker-compose.yml
    ├── .env.example.local
    ├── .env.example.railway
    └── README.md
```

## 🎯 Probar Reto 1 - User Service

### 1. Levantar el servicio

```bash
cd reto1_user_service
docker-compose up --build
```

### 2. Probar API (en otra terminal)

```bash
# Crear usuario
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mario Pazmiño",
    "email": "mario@example.com",
    "password": "securepass123"
  }'

# Guardar el ID que retorna y usarlo aquí:
# Consultar usuario
curl http://localhost:8000/users/{ID_DEL_USUARIO}
```

### 3. Ver documentación

Abrir en navegador: http://localhost:8000/docs

## 🎯 Probar Reto 2 - Microservicios

### 1. Levantar todos los servicios

```bash
cd reto2_microservices
docker-compose up --build
```

**Esto levanta:**
- MongoDB (puerto 27017)
- RabbitMQ (puerto 5672, UI: 15672)
- Orders Service (puerto 8001)
- Notifications Service (consumer)

### 2. Crear una orden

```bash
curl -X POST "http://localhost:8001/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop HP Pavilion",
    "quantity": 2,
    "customer_email": "customer@example.com"
  }'
```

### 3. Ver la notificación

En los logs de docker-compose verás:

```
notifications_service  | 📧 New order received: 65a1b2c3d4e5f6g7h8i9j0k1
notifications_service  |    Product: Laptop HP Pavilion
notifications_service  |    Quantity: 2
notifications_service  |    Customer: customer@example.com
```

### 4. Ver RabbitMQ Management

Abrir: http://localhost:15672
- Usuario: `guest`
- Password: `guest`

### 5. Ver documentación

Abrir: http://localhost:8001/docs

## 📦 Comandos Útiles

### Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Solo notifications
docker-compose logs -f notifications_service

# Solo orders
docker-compose logs -f orders_service
```

### Detener servicios

```bash
# Detener
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Reiniciar un servicio específico

```bash
docker-compose restart orders_service
docker-compose restart notifications_service
```

## 🌐 Despliegue en Railway

### Reto 1 - User Service

1. **Crear MongoDB Atlas:**
   - https://www.mongodb.com/cloud/atlas
   - Crear cluster M0 (gratis)
   - Network Access: 0.0.0.0/0
   - Copiar connection string

2. **Desplegar en Railway:**
   - Crear nuevo servicio desde GitHub
   - Root Directory: `reto1_user_service`
   - Variables de entorno:
     ```
     MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/users_db
     DATABASE_NAME=users_db
     ```

### Reto 2 - Microservicios

1. **Crear MongoDB Atlas** (mismo proceso)

2. **Crear CloudAMQP:**
   - https://www.cloudamqp.com
   - Crear instancia "Little Lemur" (gratis)
   - Copiar AMQP URL

3. **Desplegar Orders Service:**
   - Root Directory: `reto2_microservices/orders_service`
   - Variables:
     ```
     MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/orders_db
     DATABASE_NAME=orders_db
     RABBITMQ_URL=amqps://user:pass@host.cloudamqp.com/vhost
     ```

4. **Desplegar Notifications Service:**
   - Root Directory: `reto2_microservices/notifications_service`
   - Variable:
     ```
     RABBITMQ_URL=amqps://user:pass@host.cloudamqp.com/vhost
     ```

## ✨ Características Implementadas

### Reto 1
- ✅ CRUD completo de usuarios
- ✅ Encriptación de contraseñas con bcrypt
- ✅ Validaciones con Pydantic v2
- ✅ MongoDB asíncrono con Motor
- ✅ Middleware de logging de tiempo de respuesta
- ✅ Documentación Swagger automática
- ✅ Mismo código para local y Railway

### Reto 2
- ✅ Orders Service con FastAPI
- ✅ Notifications Service (consumer)
- ✅ RabbitMQ para comunicación asíncrona
- ✅ MongoDB para persistencia
- ✅ Manejo robusto de errores
- ✅ Logs detallados
- ✅ Docker Compose funcional
- ✅ Mismo código para local y Railway

## 📚 Recursos

- [README Principal](./README.md)
- [README Reto 1](./reto1_user_service/README.md)
- [README Reto 2](./reto2_microservices/README.md)

## 🤝 Ayuda

Si tienes problemas:

1. Verifica que Docker esté corriendo
2. Revisa los logs: `docker-compose logs`
3. Reinicia los servicios: `docker-compose down && docker-compose up --build`
4. Verifica las variables de entorno

## 👨‍💻 Autor

Mario Pazmiño - 2025
