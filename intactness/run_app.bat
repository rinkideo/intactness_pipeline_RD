@echo off
setlocal

if "%IMAGE_NAME%"=="" set IMAGE_NAME=ghcr.io/rinkideo/intactness-app:latest
set COMPOSE_FILE=docker-compose.app.yml

where docker >nul 2>nul
if errorlevel 1 (
  echo Docker is not installed or not on PATH.
  echo Install Docker Desktop, then rerun this script.
  exit /b 1
)

echo Pulling app image: %IMAGE_NAME%
docker pull %IMAGE_NAME%
if errorlevel 1 exit /b 1

echo Starting Intactness app
docker compose -f %COMPOSE_FILE% up -d
if errorlevel 1 exit /b 1

timeout /t 4 /nobreak >nul
start http://localhost:8501

echo.
echo App is opening at http://localhost:8501
echo To stop it later: docker compose -f %COMPOSE_FILE% down
endlocal
