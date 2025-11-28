@echo off
echo ==========================================
echo      CONFIGURANDO AMBIENTE WINDOWS
echo ==========================================

REM --- 1. SOAP Service ---
echo.
echo [1/5] Configurando SOAP (Python)...
cd src\soap-frete-service
if not exist venv (
    echo Criando venv...
    python -m venv venv
)
echo Instalando dependencias...
call venv\Scripts\activate
pip install -r requirements.txt
call deactivate
cd ..\..

REM --- 2. Django Catalogo ---
echo.
echo [2/5] Configurando Django (Python)...
cd src\api-catalogo-django
if not exist venv (
    echo Criando venv...
    python -m venv venv
)
echo Instalando dependencias...
call venv\Scripts\activate
pip install -r requirements.txt
call deactivate
cd ..\..

REM --- 3. Gateway FastAPI ---
echo.
echo [3/5] Configurando Gateway (Python)...
cd src\api-gateway-fastapi
if not exist venv (
    echo Criando venv...
    python -m venv venv
)
echo Instalando dependencias...
call venv\Scripts\activate
pip install -r requirements.txt
call deactivate
cd ..\..

REM --- 4. Node Express ---
echo.
echo [4/5] Configurando Express (Node)...
cd src\api-logistica-express
call npm install
cd ..\..

REM --- 5. Vue Frontend ---
echo.
echo [5/5] Configurando Vue (Node)...
cd src\loja-vue
call npm install
cd ..\..

echo.
echo ==========================================
echo        INSTALACAO CONCLUIDA!
echo ==========================================
pause