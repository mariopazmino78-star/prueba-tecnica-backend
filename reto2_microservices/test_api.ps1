# Script de prueba rápida para Reto 2 - Microservices (PowerShell)
# Ejecutar después de: docker-compose up --build

Write-Host "🧪 Probando Microservices API..." -ForegroundColor Cyan
Write-Host ""

# URL base
$BASE_URL = "http://localhost:8001"

Write-Host "1️⃣ Health Check..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$BASE_URL/health" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "2️⃣ Creando orden #1..." -ForegroundColor Yellow
$order1 = @{
    product_name = "Laptop HP Pavilion 15"
    quantity = 2
    customer_email = "customer1@example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$BASE_URL/orders/" -Method Post -Body $order1 -ContentType "application/json" | ConvertTo-Json
Write-Host ""

Write-Host "⏳ Esperando 2 segundos..." -ForegroundColor Gray
Start-Sleep -Seconds 2

Write-Host "3️⃣ Creando orden #2..." -ForegroundColor Yellow
$order2 = @{
    product_name = "Mouse Logitech MX Master 3"
    quantity = 1
    customer_email = "customer2@example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$BASE_URL/orders/" -Method Post -Body $order2 -ContentType "application/json" | ConvertTo-Json
Write-Host ""

Write-Host "⏳ Esperando 2 segundos..." -ForegroundColor Gray
Start-Sleep -Seconds 2

Write-Host "4️⃣ Creando orden #3..." -ForegroundColor Yellow
$order3 = @{
    product_name = "Teclado Mecánico Keychron K2"
    quantity = 3
    customer_email = "customer3@example.com"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "$BASE_URL/orders/" -Method Post -Body $order3 -ContentType "application/json"
$response | ConvertTo-Json
$ORDER_ID = $response.id
Write-Host ""

Write-Host "5️⃣ Consultando última orden creada (ID: $ORDER_ID)..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$BASE_URL/orders/$ORDER_ID" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "✅ Pruebas completadas!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Verifica los logs del notifications_service con:" -ForegroundColor Cyan
Write-Host "   docker-compose logs notifications_service" -ForegroundColor White
Write-Host ""
Write-Host "📖 Ver documentación interactiva en: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "🐰 Ver RabbitMQ Management UI en: http://localhost:15672 (guest/guest)" -ForegroundColor Cyan
