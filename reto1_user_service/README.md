# Reto 1: User Service - CRUD de Usuarios

API REST completa para gestión de usuarios utilizando FastAPI y MongoDB con operaciones CRUD, encriptación de contraseñas y middleware de logging.

## 🎯 Características

- ✅ **CRUD Completo**: Create, Read, Update, Delete de usuarios
- ✅ **Seguridad**: Encriptación de contraseñas con bcrypt
- ✅ **Validaciones**: Pydantic v2 para validación de datos
- ✅ **Async**: MongoDB asíncrono con Motor
- ✅ **Middleware**: Medición de tiempo de respuesta
- ✅ **Documentación**: Swagger UI automática en `/docs`
- ✅ **Logging**: Logs detallados en consola
- ✅ **Portable**: Mismo código para local y Railway

## 🏗️ Estructura

```
reto1_user_service/
├── main.py                 # Aplicación FastAPI principal
├── models/
│   └── user.py            # Modelos Pydantic
├── routes/
│   └── user_routes.py     # Endpoints CRUD
├── config/
│   └── database.py        # Conexión MongoDB
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Inicio Rápido

### Opción 1: Con Docker Compose (Recomendado)

```bash
# Clonar el repositorio y navegar al directorio
cd reto1_user_service

# Copiar archivo de variables de entorno
cp .env.example .env

# Levantar todos los servicios
docker-compose up --build

# La API estará disponible en:
# http://localhost:8000
# Documentación: http://localhost:8000/docs
```

### Opción 2: Manualmente (requiere MongoDB local)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export MONGODB_URI="mongodb://localhost:27017"
export DATABASE_NAME="users_db"

# Ejecutar aplicación
uvicorn main:app --reload

# O con Python
python main.py
```

## 📋 API Endpoints

### 1. Crear Usuario
**POST** `/users/`

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Respuesta (201 Created):**
```json
{
  "id": "65a1b2c3d4e5f6g7h8i9j0k1",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### 2. Obtener Usuario
**GET** `/users/{user_id}`

```bash
curl -X GET "http://localhost:8000/users/65a1b2c3d4e5f6g7h8i9j0k1"
```

**Respuesta (200 OK):**
```json
{
  "id": "65a1b2c3d4e5f6g7h8i9j0k1",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### 3. Actualizar Usuario
**PUT** `/users/{user_id}`

```bash
curl -X PUT "http://localhost:8000/users/65a1b2c3d4e5f6g7h8i9j0k1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "johnsmith@example.com"
  }'
```

**Nota:** Todos los campos son opcionales. Solo se actualizan los campos enviados.

### 4. Eliminar Usuario
**DELETE** `/users/{user_id}`

```bash
curl -X DELETE "http://localhost:8000/users/65a1b2c3d4e5f6g7h8i9j0k1"
```

**Respuesta:** 204 No Content

## 🌐 Despliegue en Railway

### 1. Configurar MongoDB Atlas

1. Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crear cluster gratuito
3. Configurar IP Access: permitir `0.0.0.0/0`
4. Obtener connection string

### 2. Configurar Railway

1. Crear nuevo proyecto en [Railway](https://railway.app)
2. Conectar repositorio de GitHub
3. Configurar variables de entorno:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/users_db?retryWrites=true&w=majority
DATABASE_NAME=users_db
```

4. Railway detectará automáticamente el `Dockerfile` y desplegará

### 3. Verificar Despliegue

```bash
# Reemplazar con tu URL de Railway
curl https://tu-app.railway.app/health
```

## 🧪 Ejemplos de Prueba

### Colección Postman

Importar en Postman:

```json
{
  "info": {
    "name": "User Service API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create User",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Jane Doe\",\n  \"email\": \"jane@example.com\",\n  \"password\": \"password123\"\n}"
        },
        "url": "{{base_url}}/users/"
      }
    },
    {
      "name": "Get User",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/users/{{user_id}}"
      }
    },
    {
      "name": "Update User",
      "request": {
        "method": "PUT",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Jane Smith\"\n}"
        },
        "url": "{{base_url}}/users/{{user_id}}"
      }
    },
    {
      "name": "Delete User",
      "request": {
        "method": "DELETE",
        "url": "{{base_url}}/users/{{user_id}}"
      }
    }
  ]
}
```

**Variables de entorno en Postman:**
- `base_url`: `http://localhost:8000` (local) o tu URL de Railway

## 📊 Características Técnicas

### Middleware de Logging

El middleware mide y registra:
- Método HTTP
- Ruta solicitada
- Código de estado de respuesta
- Tiempo de procesamiento en milisegundos

**Ejemplo de log:**
```
2025-01-15 10:30:45 - __main__ - INFO - 📊 POST /users/ - Status: 201 - Time: 45.32ms
```

### Validaciones Pydantic

- **Email**: Validación de formato con `EmailStr`
- **Password**: Mínimo 6 caracteres
- **Name**: Entre 1 y 100 caracteres
- **ObjectId**: Validación de formato MongoDB

### Seguridad

- Contraseñas encriptadas con bcrypt (salt rounds: 12)
- Nunca se retorna el password en respuestas
- Validación de emails únicos
- Manejo seguro de errores (sin exponer detalles internos)

## 🔧 Variables de Entorno

| Variable | Descripción | Ejemplo Local | Ejemplo Railway |
|----------|-------------|---------------|-----------------|
| `MONGODB_URI` | URI de conexión a MongoDB | `mongodb://mongodb:27017` | `mongodb+srv://user:pass@cluster.mongodb.net` |
| `DATABASE_NAME` | Nombre de la base de datos | `users_db` | `users_db` |

## 📝 Notas Importantes

1. **Mismo Código**: El código es idéntico para local y Railway, solo cambian las variables de entorno
2. **Async**: Todas las operaciones de base de datos son asíncronas
3. **Error Handling**: Manejo robusto de errores con try/except y códigos HTTP apropiados
4. **Logs**: Logging detallado para debugging y monitoreo
5. **CORS**: Configurado para aceptar peticiones desde cualquier origen (ajustar en producción)

## 🐛 Troubleshooting

### MongoDB no conecta en Docker

```bash
# Verificar que MongoDB esté corriendo
docker-compose ps

# Ver logs de MongoDB
docker-compose logs mongodb

# Reiniciar servicios
docker-compose down
docker-compose up --build
```

### Error de conexión en Railway

1. Verificar que la IP `0.0.0.0/0` esté permitida en MongoDB Atlas
2. Verificar que el connection string incluya el nombre de la base de datos
3. Revisar logs en Railway dashboard

## 📄 Licencia

Proyecto de prueba técnica - 2025

## 👨‍💻 Autor

Mario Pazmiño
