#!/bin/bash
# Script de prueba rápida para Reto 1 - User Service
# Ejecutar después de: docker-compose up --build

echo "🧪 Probando User Service API..."
echo ""

# URL base
BASE_URL="http://localhost:8000"

echo "1️⃣ Health Check..."
curl -s $BASE_URL/health | python -m json.tool
echo -e "\n"

echo "2️⃣ Creando usuario..."
RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mario Pazmiño",
    "email": "mario.pazmino@example.com",
    "password": "securepass123"
  }')

echo $RESPONSE | python -m json.tool
USER_ID=$(echo $RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo -e "\n"

echo "3️⃣ Consultando usuario creado (ID: $USER_ID)..."
curl -s "$BASE_URL/users/$USER_ID" | python -m json.tool
echo -e "\n"

echo "4️⃣ Actualizando usuario..."
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mario Pazmiño - UPDATED"
  }' | python -m json.tool
echo -e "\n"

echo "5️⃣ Verificando actualización..."
curl -s "$BASE_URL/users/$USER_ID" | python -m json.tool
echo -e "\n"

echo "6️⃣ Eliminando usuario..."
curl -s -X DELETE "$BASE_URL/users/$USER_ID" -w "HTTP Status: %{http_code}\n"
echo -e "\n"

echo "7️⃣ Verificando eliminación (debe dar 404)..."
curl -s "$BASE_URL/users/$USER_ID" | python -m json.tool
echo -e "\n"

echo "✅ Pruebas completadas!"
echo "📖 Ver documentación interactiva en: http://localhost:8000/docs"
