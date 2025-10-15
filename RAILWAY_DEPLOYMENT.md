# 🚂 Guía de Despliegue en Railway - Prueba Técnica Backend

Esta guía te llevará paso a paso para desplegar **ambos retos** en Railway.

---

## 📋 Prerequisitos

Antes de comenzar, necesitas crear cuentas gratuitas en:

1. ✅ **Railway**: https://railway.app (login con GitHub)
2. ✅ **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas (gratis)
3. ✅ **CloudAMQP**: https://www.cloudamqp.com (solo para Reto 2)

---

## 🎯 RETO 1: User Service

### Paso 1: Crear MongoDB en Atlas

1. Ir a https://cloud.mongodb.com
2. Click en **"Create"** para nuevo cluster
3. Seleccionar **M0 (FREE)**
4. Región: Elegir la más cercana (ej: `us-east-1`)
5. Cluster Name: `prueba-tecnica`
6. Click **"Create Cluster"** (tarda 3-5 minutos)

### Paso 2: Configurar Acceso a MongoDB

1. **Network Access**:
   - Click en "Network Access" en el menú izquierdo
   - Click **"Add IP Address"**
   - Click **"Allow Access from Anywhere"** → `0.0.0.0/0`
   - Click **"Confirm"**

2. **Database User**:
   - Click en "Database Access"
   - Click **"Add New Database User"**
   - Username: `admin`
   - Password: Generar una segura (copiar y guardar)
   - Database User Privileges: **"Read and write to any database"**
   - Click **"Add User"**

3. **Obtener Connection String**:
   - Click en "Database" → "Connect"
   - Seleccionar **"Connect your application"**
   - Driver: **Python**, Version: **3.11 or later**
   - Copiar el connection string:
   ```
   mongodb+srv://admin:<password>@prueba-tecnica.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   - Reemplazar `<password>` con tu password real

### Paso 3: Desplegar User Service en Railway

1. Ir a https://railway.app
2. Click **"New Project"**
3. Seleccionar **"Deploy from GitHub repo"**
4. Autorizar acceso a tu repositorio: `mariopazmino78-star/prueba-tecnica-backend`
5. Railway detectará múltiples servicios, seleccionar **manualmente**:

**Configuración del Servicio:**
- Service Name: `user-service`
- Root Directory: `reto1_user_service`
- Build Command: (automático, usa Dockerfile)
- Start Command: (automático desde Dockerfile)

### Paso 4: Configurar Variables de Entorno (Reto 1)

En Railway, ir a tu servicio `user-service` → **Variables**:

```bash
MONGODB_URI=mongodb+srv://admin:TU_PASSWORD@prueba-tecnica.xxxxx.mongodb.net/users_db?retryWrites=true&w=majority
DATABASE_NAME=users_db
```

**⚠️ IMPORTANTE**: Reemplazar `TU_PASSWORD` con tu password real de MongoDB Atlas.

### Paso 5: Verificar Despliegue (Reto 1)

1. Railway generará una URL automáticamente (ej: `https://user-service-production.up.railway.app`)
2. Probar el endpoint de health:
   ```bash
   curl https://TU_URL.railway.app/health
   ```

3. Probar crear un usuario:
   ```bash
   curl -X POST "https://TU_URL.railway.app/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test User",
       "email": "test@example.com",
       "password": "password123"
     }'
   ```

4. Ver Swagger Docs:
   ```
   https://TU_URL.railway.app/docs
   ```

---

## 🎯 RETO 2: Microservicios con RabbitMQ

### Paso 1: Crear MongoDB para Orders (Atlas)

Opción A: **Usar el mismo cluster del Reto 1** (Recomendado)
- Solo usar una base de datos diferente: `orders_db`

Opción B: **Crear un cluster nuevo**
- Seguir los mismos pasos del Reto 1
- Cluster Name: `orders-cluster`

**Connection String para Reto 2:**
```
mongodb+srv://admin:<password>@prueba-tecnica.xxxxx.mongodb.net/orders_db?retryWrites=true&w=majority
```

### Paso 2: Crear RabbitMQ en CloudAMQP

1. Ir a https://www.cloudamqp.com
2. Click **"Sign Up"** (o login si ya tienes cuenta)
3. Crear nueva instancia:
   - Name: `prueba-tecnica-rabbitmq`
   - Plan: **Little Lemur (Free)**
   - Region: Elegir la más cercana (ej: `US-East-1`)
   - Click **"Select Region"**

4. **Obtener AMQP URL**:
   - Click en tu instancia recién creada
   - En el panel principal verás la **AMQP URL**:
   ```
   amqps://usuario:password@servidor.cloudamqp.com/vhost
   ```
   - Copiar esta URL completa

### Paso 3: Desplegar Orders Service en Railway

1. En tu proyecto de Railway, click **"New Service"**
2. Seleccionar **"GitHub Repo"** → `prueba-tecnica-backend`
3. Configurar:
   - Service Name: `orders-service`
   - Root Directory: `reto2_microservices/orders_service`

### Paso 4: Configurar Variables de Entorno (Orders Service)

En Railway → `orders-service` → **Variables**:

```bash
MONGODB_URI=mongodb+srv://admin:TU_PASSWORD@prueba-tecnica.xxxxx.mongodb.net/orders_db?retryWrites=true&w=majority
DATABASE_NAME=orders_db
RABBITMQ_URL=amqps://usuario:password@servidor.cloudamqp.com/vhost
```

### Paso 5: Desplegar Notifications Service en Railway

1. En tu proyecto de Railway, click **"New Service"**
2. Seleccionar **"GitHub Repo"** → `prueba-tecnica-backend`
3. Configurar:
   - Service Name: `notifications-service`
   - Root Directory: `reto2_microservices/notifications_service`

### Paso 6: Configurar Variables de Entorno (Notifications Service)

En Railway → `notifications-service` → **Variables**:

```bash
RABBITMQ_URL=amqps://usuario:password@servidor.cloudamqp.com/vhost
```

**Nota**: Este servicio NO necesita MongoDB, solo RabbitMQ.

### Paso 7: Verificar Despliegue (Reto 2)

1. **Probar Orders Service**:
   ```bash
   curl -X POST "https://TU_ORDERS_SERVICE.railway.app/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "product_name": "Test Product",
       "quantity": 1,
       "customer_email": "test@example.com"
     }'
   ```

2. **Ver logs de Notifications Service** en Railway:
   - Ir a `notifications-service` → **Deployments** → **View Logs**
   - Deberías ver: `📧 New order received: {order_id}`

3. **Ver Swagger Docs**:
   ```
   https://TU_ORDERS_SERVICE.railway.app/docs
   ```

---

## 📊 Resumen de Servicios Desplegados

| Servicio | URL Railway | Base de Datos | Message Broker |
|----------|-------------|---------------|----------------|
| **User Service** | `https://user-service.railway.app` | MongoDB Atlas (users_db) | - |
| **Orders Service** | `https://orders-service.railway.app` | MongoDB Atlas (orders_db) | CloudAMQP |
| **Notifications Service** | Sin URL pública (solo logs) | - | CloudAMQP |

---

## 🔍 Monitoreo y Verificación

### MongoDB Atlas
1. Ir a tu cluster en Atlas
2. Click **"Collections"**
3. Verificar que existen:
   - Database: `users_db` → Collection: `users`
   - Database: `orders_db` → Collection: `orders`

### CloudAMQP Dashboard
1. Ir a tu instancia en CloudAMQP
2. Click en **"RabbitMQ Manager"**
3. Ver:
   - Queues: Debería aparecer `orders_queue`
   - Connections: Debería mostrar 2 conexiones (orders-service y notifications-service)

### Railway Logs
Cada servicio en Railway tiene logs en tiempo real:
- Click en el servicio → **Deployments** → **View Logs**

---

## ⚠️ Troubleshooting

### Error: "Could not connect to MongoDB"
- Verificar que la IP `0.0.0.0/0` está permitida en Network Access
- Verificar que el password en el connection string es correcto (sin `<` `>`)
- Verificar que el database name está en el connection string

### Error: "Could not connect to RabbitMQ"
- Verificar que la AMQP URL es completa (empieza con `amqps://`)
- Verificar que no hay espacios al copiar la URL
- Verificar en CloudAMQP que la instancia está "Running"

### Notifications Service no muestra logs
- Verificar que Orders Service publicó un mensaje correctamente
- Verificar que ambos servicios usan la **misma** RABBITMQ_URL
- Revisar logs de Notifications Service en Railway

### Error: "Port already in use" en Railway
- Railway asigna puertos automáticamente, este error NO debería aparecer
- Si aparece, verificar que el Dockerfile expone el puerto correcto
- Para Orders Service debe ser puerto `8002`

---

## 📝 Checklist Final

Antes de entregar la prueba técnica:

### Reto 1 - User Service
- [ ] MongoDB Atlas creado y configurado
- [ ] User Service desplegado en Railway
- [ ] Variables de entorno configuradas
- [ ] Endpoint `/health` responde
- [ ] Swagger Docs (`/docs`) accesible
- [ ] CRUD de usuarios funciona (probar con Postman/curl)

### Reto 2 - Microservicios
- [ ] MongoDB Atlas para orders configurado
- [ ] CloudAMQP creado y configurado
- [ ] Orders Service desplegado en Railway
- [ ] Notifications Service desplegado en Railway
- [ ] Variables de entorno configuradas en ambos servicios
- [ ] POST /orders crea orden en MongoDB
- [ ] Logs de Notifications Service muestran "New order received: {order_id}"
- [ ] Swagger Docs de Orders Service accesible

---

## 🎯 URLs para Entregar

Al finalizar, tendrás estas URLs para compartir:

```
# RETO 1
User Service API: https://[tu-user-service].up.railway.app
User Service Docs: https://[tu-user-service].up.railway.app/docs

# RETO 2
Orders Service API: https://[tu-orders-service].up.railway.app
Orders Service Docs: https://[tu-orders-service].up.railway.app/docs

# Repositorio GitHub
https://github.com/mariopazmino78-star/prueba-tecnica-backend
```

---

## 💡 Consejos Finales

1. **No commitear credenciales**: Las variables de entorno se configuran solo en Railway
2. **Probar todo localmente primero**: Asegurarte que funciona con `docker-compose up`
3. **Ver logs constantemente**: Railway tiene logs en tiempo real muy útiles
4. **Free tier limits**:
   - Railway: $5 de crédito mensual
   - MongoDB Atlas: 512 MB de almacenamiento
   - CloudAMQP: 1 millón de mensajes/mes
5. **Documentar las URLs**: Guardar todas las URLs en un documento para la entrega

---

## 🚀 ¡Listo para Desplegar!

Ahora tienes todo lo necesario para desplegar ambos retos en Railway. Sigue los pasos en orden y verifica cada uno antes de continuar al siguiente.

**¿Necesitas ayuda?** Contacta al evaluador con:
- Screenshots de los errores
- Logs de Railway
- Variables de entorno configuradas (sin mostrar passwords reales)

---

**Autor**: Mario Pazmiño  
**Fecha**: Octubre 2025  
**Repositorio**: https://github.com/mariopazmino78-star/prueba-tecnica-backend
