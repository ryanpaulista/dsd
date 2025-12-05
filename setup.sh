#!/bin/bash

BASE_DIR=$(pwd)

echo "=========================================="
echo "   CONFIGURANDO AMBIENTE LINUX (DOCKER)"
echo "=========================================="

# Verifica se o Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ [ERRO] O Docker não está rodando ou você não tem permissão."
    echo "Tente iniciar o serviço: sudo systemctl start docker"
    exit 1
fi

# --- 1. SOAP Service (DOCKER BUILD) ---
echo ""
echo "🐳 [1/5] Construindo Imagem Docker para SOAP..."
cd "$BASE_DIR/src/soap-frete-service"
docker build -t soap-frete .
if [ $? -ne 0 ]; then
    echo "❌ Falha ao criar imagem Docker."
    exit 1
fi

# --- 2. Django Catálogo ---
echo ""
echo "🐍 [2/5] Configurando Django (Python Local)..."
cd "$BASE_DIR/src/api-catalogo-django"
if [ ! -d "venv" ]; then python3 -m venv venv; fi
source venv/bin/activate
pip install -r requirements.txt
deactivate

# --- 3. Gateway FastAPI ---
echo ""
echo "⚡ [3/5] Configurando Gateway (Python Local)..."
cd "$BASE_DIR/src/api-gateway-fastapi"
if [ ! -d "venv" ]; then python3 -m venv venv; fi
source venv/bin/activate
pip install -r requirements.txt
deactivate

# --- 4. Node Express ---
echo ""
echo "🟢 [4/5] Configurando Express (Node)..."
cd "$BASE_DIR/src/api-logistica-express"
npm install

# --- 5. Vue Frontend ---
echo ""
echo "💻 [5/5] Configurando Vue (Node)..."
cd "$BASE_DIR/src/loja-vue"
npm install

echo ""
echo "=========================================="
echo "✅  INSTALAÇÃO CONCLUÍDA!"
echo "=========================================="