@echo off
echo ==========================================
echo    INICIANDO BRAINZ E-SHOP (HIBRIDO)
echo ==========================================

REM 1. Inicia SOAP (Via DOCKER na porta 8000)
REM Remove container anterior se existir para evitar conflito de nome
docker rm -f soap-container >nul 2>&1
echo Iniciando Container SOAP...
start "1. SOAP Service (DOCKER)" cmd /k "docker run --name soap-container -p 8000:8000 -it soap-frete"

REM 2. Inicia Django (Porta 8001)
timeout /t 3 >nul
start "2. Django Catalogo" cmd /k "cd src\api-catalogo-django & call venv\Scripts\activate & echo Iniciando Django... & python manage.py runserver 0.0.0.0:8001"

REM 3. Inicia Express (Porta 3000)
timeout /t 2 >nul
start "3. Logistica Node" cmd /k "cd src\api-logistica-express & echo Iniciando Node... & node server.js"

REM 4. Inicia Gateway (Porta 8080)
timeout /t 2 >nul
start "4. API Gateway" cmd /k "cd src\api-gateway-fastapi & call venv\Scripts\activate & echo Iniciando Gateway... & uvicorn main:app --host 0.0.0.0 --port 8080 --reload"

REM 5. Inicia Vue (Porta 5173)
timeout /t 2 >nul
start "5. Vue Frontend" cmd /k "cd src\loja-vue & echo Iniciando Vue... & npm run dev"

echo.
echo Todos os servicos foram iniciados!
echo SOAP esta rodando isolado no Docker.
echo Boa apresentacao!
pause