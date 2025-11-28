@echo off
echo ==========================================
echo    INICIANDO BRAINZ E-SHOP (WINDOWS)
echo ==========================================

REM Pega o diretorio atual
set "BASE_DIR=%cd%"

REM 1. Inicia SOAP (Porta 8000)
start "1. SOAP Service" cmd /k "cd src\soap-frete-service & call venv\Scripts\activate & echo Iniciando SOAP... & python main.py"

REM 2. Inicia Django (Porta 8001)
REM Timeout de 2 segundos para dar tempo do SOAP subir (opcional)
timeout /t 2 >nul
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
echo Todos os servicos foram iniciados em janelas separadas.
echo Boa apresentacao!
pause