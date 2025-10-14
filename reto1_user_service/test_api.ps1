# Script de prueba rapida para Reto 1 - User Service (PowerShell)
# Ejecutar despues de: docker-compose up --build

Write-Host "Probando User Service API..." -ForegroundColor Cyan
Write-Host ""

# URL base
$BASE_URL = "http://localhost:8000"

Write-Host "1. Health Check..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$BASE_URL/health" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "2. Creando usuario..." -ForegroundColor Yellow

# Generar email unico con timestamp
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$email = "mario.test.$timestamp@example.com"

$body = @{
    name = "Mario Pazmino"
    email = $email
    password = "securepass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "$BASE_URL/users/" -Method Post -Body $body -ContentType "application/json"
$response | ConvertTo-Json
$USER_ID = $response._id
Write-Host ""
Write-Host "Usuario creado con ID: $USER_ID" -ForegroundColor Green
Write-Host ""

Write-Host "3. Consultando usuario creado (ID: $USER_ID)..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "4. Actualizando usuario..." -ForegroundColor Yellow
$updateBody = @{
    name = "Mario Pazmino - UPDATED"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Put -Body $updateBody -ContentType "application/json" | ConvertTo-Json
Write-Host ""

Write-Host "5. Verificando actualizacion..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "6. Eliminando usuario..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Delete
    Write-Host "Usuario eliminado (204 No Content)" -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "7. Verificando eliminacion (debe dar 404)..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "$BASE_URL/users/$USER_ID" -Method Get
} catch {
    Write-Host "Error 404 esperado - Usuario no encontrado" -ForegroundColor Green
}
Write-Host ""

Write-Host "Pruebas completadas!" -ForegroundColor Green
Write-Host "Ver documentacion interactiva en: http://localhost:8000/docs" -ForegroundColor Cyan
