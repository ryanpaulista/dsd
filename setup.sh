#!/bin/bash

# Pega o diretório atual onde o script está
BASE_DIR=$(pwd)

echo "🛠️  INICIANDO PREPARAÇÃO DO AMBIENTE..."

# --- 1. SOAP Service (Python) ---
echo "--------------------------------------------------"
echo "📦 Configurando: SOAP Frete (Python)..."
cd "$BASE_DIR/src/soap-frete-service"
# Cria venv se não existir
if [ ! -d "venv" ]; then python3 -m venv venv; fi
# Ativa, instala e desativa
source venv/bin/activate
pip install -r requirements.txt
deactivate

# --- 2. Django Catálogo (Python) ---
echo "--------------------------------------------------"
echo "📦 Configurando: Catálogo Django (Python)..."
cd "$BASE_DIR/src/api-catalogo-django"
if [ ! -d "venv" ]; then python3 -m venv venv; fi
source venv/bin/activate
pip install -r requirements.txt
deactivate

# --- 3. Gateway FastAPI (Python) ---
echo "--------------------------------------------------"
echo "📦 Configurando: API Gateway (Python)..."
cd "$BASE_DIR/src/api-gateway-fastapi"
if [ ! -d "venv" ]; then python3 -m venv venv; fi
source venv/bin/activate
pip install -r requirements.txt
deactivate

# --- 4. Logística Express (Node) ---
echo "--------------------------------------------------"
echo "📦 Configurando: Logística Express (Node)..."
cd "$BASE_DIR/src/api-logistica-express"
npm install

# --- 5. Loja Vue (Node) ---
echo "--------------------------------------------------"
echo "📦 Configurando: Frontend Vue (Node)..."
cd "$BASE_DIR/src/loja-vue"
npm install

echo "--------------------------------------------------"
echo "✅ CONFIGURAÇÃO CONCLUÍDA! Use ./start.sh para rodar."