# Script de prueba rápida para Reto 1 - User Service (PowerShell)
# Ejecutar después de: docker-compose up --build

Write-Host "🧪 Probando User Service API..." -ForegroundColor Cyan
Write-Host ""

# URL base
$BASE_URL = "http://localhost:8000"

Write-Host "1️⃣ Health Check..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$BASE_URL/health" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "2️⃣ Creando usuario..." -ForegroundColor Yellow
$body = @{
    name = "Mario Pazmiño"
    email = "mario.pazmino@example.com"
    password = "securepass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "$BASE_URL/users/" -Method Post -Body $body -ContentType "application/json"
$response | ConvertTo-Json
$USER_ID = $response.id
Write-Host ""

Write-Host "3️⃣ Consultando usuario creado (ID: $USER_ID)..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "4️⃣ Actualizando usuario..." -ForegroundColor Yellow
$updateBody = @{
    name = "Mario Pazmiño - UPDATED"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Put -Body $updateBody -ContentType "application/json" | ConvertTo-Json
Write-Host ""

Write-Host "5️⃣ Verificando actualización..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "6️⃣ Eliminando usuario..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Delete
    Write-Host "Usuario eliminado (204 No Content)" -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "7️⃣ Verificando eliminación (debe dar 404)..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Get
} catch {
    Write-Host "✅ Error 404 esperado - Usuario no encontrado" -ForegroundColor Green
}
Write-Host ""

Write-Host "✅ Pruebas completadas!" -ForegroundColor Green
Write-Host "📖 Ver documentación interactiva en: http://localhost:8000/docs" -ForegroundColor Cyan
