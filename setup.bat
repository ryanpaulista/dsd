@echo off
echo ==========================================
echo   CONFIGURANDO AMBIENTE (COM DOCKER)
echo ==========================================

REM Verifica se o Docker está rodando
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO CRITICO] O Docker Desktop nao esta rodando!
    echo Por favor, inicie o Docker Desktop e aguarde a baleia ficar verde.
    pause
    exit /b
)

REM --- 1. SOAP Service (DOCKER BUILD) ---
echo.
echo [1/5] Construindo Imagem Docker para SOAP...
cd src\soap-frete-service
docker build -t soap-frete .
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar imagem Docker.
    pause
    exit /b
)
cd ..\..

REM --- 2. Django Catalogo ---
echo.
echo [2/5] Configurando Django (Python Local)...
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
echo [3/5] Configurando Gateway (Python Local)...
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