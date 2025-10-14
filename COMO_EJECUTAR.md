# ⚡ CÓMO EJECUTAR LA PRUEBA TÉCNICA

## 🎯 Opción 1: Prueba Rápida (5 minutos)

### Paso 1: Abrir una terminal en el proyecto

```powershell
cd "C:\Users\mario\Documents\Nueva carpeta\prueba-tecnica-backend"
```

### Paso 2: Elegir qué reto probar

#### 🔵 RETO 1 - User Service (CRUD)

```powershell
# Ir al directorio
cd reto1_user_service

# Levantar servicios
docker-compose up --build
```

**Espera a ver estos logs:**
```
✅ Successfully connected to MongoDB database: users_db
🚀 Starting User Service...
```

**Luego abre en tu navegador:**
- 📖 Documentación Swagger: http://localhost:8000/docs
- 🧪 Prueba manual los endpoints desde Swagger

**O ejecuta el script de pruebas:**
```powershell
# En otra terminal (mientras docker-compose sigue corriendo)
cd reto1_user_service
.\test_api.ps1
```

---

#### 🟢 RETO 2 - Microservices (RabbitMQ)

```powershell
# Ir al directorio
cd reto2_microservices

# Levantar servicios
docker-compose up --build
```

**Espera a ver estos logs:**
```
✅ Successfully connected to MongoDB database: orders_db
✅ Successfully connected to RabbitMQ
👂 Starting to listen for orders...
```

**Luego abre en tu navegador:**
- 📖 API Docs: http://localhost:8001/docs
- 🐰 RabbitMQ UI: http://localhost:15672 (usuario: guest, password: guest)

**Ejecuta el script de pruebas:**
```powershell
# En otra terminal
cd reto2_microservices
.\test_api.ps1
```

**Observa los logs del notifications service:**
```
📧 New order received: 65a1b2c3d4e5f6g7h8i9j0k1
   Product: Laptop HP Pavilion
   Quantity: 2
   Customer: customer@example.com
✅ Order 65a1b2c3d4e5f6g7h8i9j0k1 processed successfully
```

---

## 🎯 Opción 2: Revisar Documentación

### Documentos principales:

1. **RESUMEN_EJECUTIVO.md** ⭐ 
   - Vista general del proyecto
   - Características implementadas
   - Stack tecnológico

2. **QUICKSTART.md**
   - Comandos rápidos para ejecutar
   - Ejemplos de curl
   - Configuración Railway

3. **reto1_user_service/README.md**
   - Documentación completa Reto 1
   - Endpoints detallados
   - Ejemplos de uso

4. **reto2_microservices/README.md**
   - Documentación completa Reto 2
   - Arquitectura de microservicios
   - Flujo de mensajes

---

## 🎯 Opción 3: Ver el Código

### Archivos principales a revisar:

**Reto 1:**
```
📁 reto1_user_service/
  📄 main.py                      # FastAPI + Middleware de logging
  📄 routes/user_routes.py        # Endpoints CRUD + bcrypt
  📄 models/user.py               # Validaciones Pydantic
  📄 config/database.py           # MongoDB async
```

**Reto 2:**
```
📁 reto2_microservices/
  📁 orders_service/
    📄 main.py                    # FastAPI
    📄 routes/orders.py           # Crear orden + publicar mensaje
    📄 config/rabbit.py           # Publisher RabbitMQ
  
  📁 notifications_service/
    📄 consumer.py                # Main del consumer
    📄 config/rabbit.py           # Escucha mensajes
```

---

## 📊 Comandos Útiles

### Ver logs en tiempo real

```powershell
# Todos los servicios
docker-compose logs -f

# Solo un servicio específico
docker-compose logs -f notifications_service
docker-compose logs -f orders_service
```

### Detener servicios

```powershell
# Detener (mantiene datos)
docker-compose down

# Detener y eliminar todo (incluye volúmenes)
docker-compose down -v
```

### Ver servicios corriendo

```powershell
docker-compose ps
```

### Reiniciar un servicio

```powershell
docker-compose restart orders_service
```

---

## 🌐 URLs Importantes

### Reto 1 - Local
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Reto 2 - Local
- Orders API: http://localhost:8001
- Docs: http://localhost:8001/docs
- RabbitMQ UI: http://localhost:15672 (guest/guest)
- MongoDB: mongodb://localhost:27017

---

## 🧪 Probar con Postman

### Importar colección

Ver ejemplos completos en:
- `reto1_user_service/README.md` (sección Postman)
- `reto2_microservices/README.md` (sección Postman)

### Variables de entorno en Postman

**Para Reto 1:**
```
base_url: http://localhost:8000
```

**Para Reto 2:**
```
base_url: http://localhost:8001
```

---

## 🚨 Troubleshooting

### Error: "Puerto ya en uso"

```powershell
# Ver qué está usando el puerto
netstat -ano | findstr :8000
netstat -ano | findstr :8001

# Matar el proceso (reemplaza PID)
taskkill /PID <PID> /F

# O cambiar puerto en docker-compose.yml
# Cambiar "8000:8000" por "8080:8000"
```

### Error: "Cannot connect to Docker daemon"

1. Verifica que Docker Desktop esté corriendo
2. Reinicia Docker Desktop
3. Ejecuta PowerShell como Administrador

### Error: MongoDB no conecta

```powershell
# Ver logs de MongoDB
docker-compose logs mongodb

# Reiniciar servicios
docker-compose down -v
docker-compose up --build
```

### Error: RabbitMQ no conecta

```powershell
# Verificar que RabbitMQ esté saludable
docker-compose ps

# Ver logs
docker-compose logs rabbitmq

# Esperar a que el health check pase
# Verás: "health: healthy" en docker-compose ps
```

---

## 📝 Checklist de Evaluación

### Reto 1 - User Service
- [ ] ✅ Servicio levanta sin errores
- [ ] ✅ Swagger UI carga en /docs
- [ ] ✅ Crear usuario funciona (POST /users)
- [ ] ✅ Obtener usuario funciona (GET /users/{id})
- [ ] ✅ Actualizar usuario funciona (PUT /users/{id})
- [ ] ✅ Eliminar usuario funciona (DELETE /users/{id})
- [ ] ✅ Logs muestran tiempo de respuesta
- [ ] ✅ Contraseña no se retorna en respuestas

### Reto 2 - Microservices
- [ ] ✅ Todos los servicios levantan
- [ ] ✅ MongoDB conecta correctamente
- [ ] ✅ RabbitMQ conecta correctamente
- [ ] ✅ Crear orden funciona (POST /orders)
- [ ] ✅ Orden se guarda en MongoDB
- [ ] ✅ Mensaje aparece en RabbitMQ
- [ ] ✅ Notifications Service recibe mensaje
- [ ] ✅ Log muestra "New order received: {id}"
- [ ] ✅ RabbitMQ Management UI funciona

---

## 🎓 Conceptos Demostrados

### Técnicos
- ✅ FastAPI (async/await)
- ✅ MongoDB con Motor (async)
- ✅ Pydantic v2 (validaciones)
- ✅ bcrypt (seguridad)
- ✅ RabbitMQ (messaging)
- ✅ Docker & Docker Compose
- ✅ Middleware (logging)
- ✅ Error handling
- ✅ Environment variables

### Arquitectura
- ✅ API REST
- ✅ CRUD operations
- ✅ Microservices
- ✅ Event-driven architecture
- ✅ Publisher-Subscriber pattern
- ✅ Asynchronous communication
- ✅ Health checks
- ✅ Logging & Observability

---

## 🆘 Ayuda Adicional

### Documentación por prioridad:

1. **RESUMEN_EJECUTIVO.md** - Empezar aquí
2. **Este archivo** - Cómo ejecutar
3. **QUICKSTART.md** - Comandos rápidos
4. **README.md de cada reto** - Detalles técnicos
5. **Código fuente** - Ver implementación

---

## ✅ Siguiente Paso

**Elige una opción:**

```powershell
# Opción A: Probar Reto 1
cd reto1_user_service
docker-compose up --build

# Opción B: Probar Reto 2
cd reto2_microservices
docker-compose up --build

# Opción C: Leer documentación
code RESUMEN_EJECUTIVO.md
```

---

**🚀 ¡Listo para ejecutar!**

**📧 Cualquier duda, revisa los README detallados de cada reto.**
