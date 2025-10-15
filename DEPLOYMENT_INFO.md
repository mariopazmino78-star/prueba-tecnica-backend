# 🚀 Información de Despliegue - Prueba Técnica Backend

## ✅ Estado General: TODOS LOS SERVICIOS FUNCIONANDO

---

## 🌐 URLs de Producción

### Reto 1 - User Service (CRUD de Usuarios)

**URL Base:** https://prueba-tecnica-backend-production-61a8.up.railway.app

**Endpoints:**
- **Documentación Swagger:** https://prueba-tecnica-backend-production-61a8.up.railway.app/docs
- **Health Check:** https://prueba-tecnica-backend-production-61a8.up.railway.app/health
- **Crear Usuario:** `POST /users/`
- **Listar Usuarios:** `GET /users/`
- **Obtener Usuario:** `GET /users/{id}`
- **Actualizar Usuario:** `PUT /users/{id}`
- **Eliminar Usuario:** `DELETE /users/{id}`

---

### Reto 2 - Orders Service (Microservicios con RabbitMQ)

**URL Base:** https://tranquil-embrace-production.up.railway.app

**Endpoints:**
- **Documentación Swagger:** https://tranquil-embrace-production.up.railway.app/docs
- **Health Check:** https://tranquil-embrace-production.up.railway.app/health
- **Crear Orden:** `POST /orders/`
- **Obtener Orden:** `GET /orders/{id}`

**Ejemplo de Request para crear orden:**
```json
{
  "product_name": "Laptop Dell XPS",
  "quantity": 2,
  "customer_email": "mario.pazmino@example.com"
}
```

---

### Reto 2 - Notifications Service (Worker Background)

**Tipo:** Consumer de RabbitMQ (no expone endpoints HTTP)

**Función:** Escucha mensajes de la cola `orders_queue` y procesa notificaciones

**Logs disponibles en:** Railway Dashboard → Notifications Service → Logs

---

## 🔧 Infraestructura Cloud

### Railway (Hosting de Aplicaciones)
- **Plan:** Developer Plan ($5/mes)
- **Servicios desplegados:** 3
  1. User Service (Reto 1)
  2. Orders Service (Reto 2)
  3. Notifications Service (Reto 2)

### MongoDB Atlas (Base de Datos)
- **Plan:** M0 Free Tier
- **Cluster:** cluster0.kioshu4.mongodb.net
- **Bases de datos:**
  - `users_db` (Reto 1)
  - `orders_db` (Reto 2)

### CloudAMQP (RabbitMQ como Servicio)
- **Plan:** Little Lemur (Free)
- **Host:** ram.lmq.cloudamqp.com
- **Virtual Host:** eqfrecgz
- **Cola:** orders_queue

---

## 🧪 Pruebas de Funcionamiento

### Test 1: Crear Usuario (Reto 1)

```bash
curl -X POST "https://prueba-tecnica-backend-production-61a8.up.railway.app/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mario Pazmiño",
    "email": "mario@example.com",
    "password": "MySecurePass123"
  }'
```

**Respuesta esperada:** 201 Created con datos del usuario

---

### Test 2: Crear Orden y Verificar Notificación (Reto 2)

**Paso 1:** Crear orden
```bash
curl -X POST "https://tranquil-embrace-production.up.railway.app/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop Dell XPS",
    "quantity": 2,
    "customer_email": "mario.pazmino@example.com"
  }'
```

**Respuesta esperada:** 201 Created con ID de orden

**Paso 2:** Verificar en logs del Notifications Service
```
📧 New order received: [order_id]
   Product: Laptop Dell XPS
   Quantity: 2
   Customer: mario.pazmino@example.com
✅ Order [order_id] processed successfully
```

---

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                        RAILWAY CLOUD                        │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │  User Service    │  │  Orders Service  │               │
│  │  (Reto 1 CRUD)   │  │  (Reto 2 API)    │               │
│  │  Port: 8000      │  │  Port: 8002      │               │
│  └────────┬─────────┘  └────────┬─────────┘               │
│           │                     │                          │
│           │                     │  ┌────────────────────┐  │
│           │                     │  │ Notifications      │  │
│           │                     │  │ Service (Worker)   │  │
│           │                     │  └──────────┬─────────┘  │
│           │                     │             │            │
└───────────┼─────────────────────┼─────────────┼────────────┘
            │                     │             │
            ▼                     ▼             ▼
     ┌─────────────┐      ┌─────────────┐  ┌──────────────┐
     │  MongoDB    │      │  MongoDB    │  │  RabbitMQ    │
     │   Atlas     │      │   Atlas     │  │  CloudAMQP   │
     │             │      │             │  │              │
     │  users_db   │      │  orders_db  │  │orders_queue  │
     └─────────────┘      └─────────────┘  └──────────────┘
```

---

## 🔐 Seguridad

- ✅ Contraseñas encriptadas con bcrypt (Reto 1)
- ✅ Validación de datos con Pydantic v2
- ✅ Conexiones seguras (HTTPS, MongoDB Atlas SSL, RabbitMQ TLS)
- ✅ Variables de entorno para credenciales
- ✅ CORS configurado

---

## 📈 Rendimiento Verificado

### Reto 1 - User Service
- ✅ Conexión exitosa a MongoDB Atlas
- ✅ CRUD completo funcional
- ✅ Tiempo de respuesta: < 100ms

### Reto 2 - Microservicios
- ✅ Orders Service: Conexión a MongoDB y RabbitMQ exitosa
- ✅ Notifications Service: Escuchando mensajes correctamente
- ✅ Flujo end-to-end verificado:
  - Orden creada → Guardada en MongoDB → Mensaje enviado a RabbitMQ → Notificación procesada
- ✅ Tiempo de procesamiento: < 500ms

---

## 🎯 Cumplimiento de Requisitos

### Reto 1: CRUD de Usuarios ✅
- [x] Crear usuarios con validaciones
- [x] Listar usuarios
- [x] Actualizar usuarios
- [x] Eliminar usuarios
- [x] Encriptación de contraseñas
- [x] Validaciones con Pydantic
- [x] Documentación Swagger

### Reto 2: Microservicios con RabbitMQ ✅
- [x] Orders Service: API REST con FastAPI
- [x] Notifications Service: Consumer de RabbitMQ
- [x] Comunicación asíncrona vía RabbitMQ
- [x] Persistencia en MongoDB
- [x] Logs de notificaciones
- [x] Arquitectura desacoplada

---

## 📞 Soporte

**Repositorio GitHub:** https://github.com/mariopazmino78-star/prueba-tecnica-backend

**Desarrollador:** Mario Pazmiño

**Fecha de Despliegue:** 15 de Octubre, 2025

---

## 🏆 Estado Final

```
✅ Reto 1: COMPLETADO Y DESPLEGADO
✅ Reto 2: COMPLETADO Y DESPLEGADO
✅ Todos los servicios: ONLINE Y FUNCIONANDO
✅ Pruebas end-to-end: EXITOSAS
```

**🎉 Sistema listo para evaluación** 🎉
