#!/bin/bash
# Script de prueba rápida para Reto 2 - Microservices
# Ejecutar después de: docker-compose up --build

echo "🧪 Probando Microservices API..."
echo ""

# URL base
BASE_URL="http://localhost:8001"

echo "1️⃣ Health Check..."
curl -s $BASE_URL/health | python -m json.tool
echo -e "\n"

echo "2️⃣ Creando orden #1..."
curl -s -X POST "$BASE_URL/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop HP Pavilion 15",
    "quantity": 2,
    "customer_email": "customer1@example.com"
  }' | python -m json.tool
echo -e "\n"

echo "⏳ Esperando 2 segundos..."
sleep 2

echo "3️⃣ Creando orden #2..."
curl -s -X POST "$BASE_URL/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Mouse Logitech MX Master 3",
    "quantity": 1,
    "customer_email": "customer2@example.com"
  }' | python -m json.tool
echo -e "\n"

echo "⏳ Esperando 2 segundos..."
sleep 2

echo "4️⃣ Creando orden #3..."
RESPONSE=$(curl -s -X POST "$BASE_URL/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Teclado Mecánico Keychron K2",
    "quantity": 3,
    "customer_email": "customer3@example.com"
  }')

echo $RESPONSE | python -m json.tool
ORDER_ID=$(echo $RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo -e "\n"

echo "5️⃣ Consultando última orden creada (ID: $ORDER_ID)..."
curl -s "$BASE_URL/orders/$ORDER_ID" | python -m json.tool
echo -e "\n"

echo "✅ Pruebas completadas!"
echo ""
echo "📋 Verifica los logs del notifications_service para ver:"
echo "   docker-compose logs notifications_service"
echo ""
echo "📖 Ver documentación interactiva en: http://localhost:8001/docs"
echo "🐰 Ver RabbitMQ Management UI en: http://localhost:15672 (guest/guest)"
