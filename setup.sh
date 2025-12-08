#!/bin/bash

BASE_DIR=$(pwd)

echo "=========================================="
echo "   CONFIGURANDO AMBIENTE LINUX (DOCKER)"
echo "=========================================="

# --- 1. SOAP Service (DOCKER BUILD) ---
echo "--------------------------------------------------"
echo "📦 Configurando: SOAP Frete (Python)..."
cd "$BASE_DIR/src/soap-frete-service"
# Cria venv se não existir
if [ ! -d "venv" ]; then python3 -m venv venv; fi
# Ativa, instala e desativa
source venv/bin/activate
pip install -r requirements.txt
deactivate

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