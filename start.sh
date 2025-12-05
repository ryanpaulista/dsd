#!/bin/bash

BASE_DIR=$(pwd)

echo "🚀 Iniciando Brainz E-Shop (Híbrido: Docker + Local)..."

# Remove container anterior para evitar conflito de nome
docker rm -f soap-container > /dev/null 2>&1

# Abre o terminal com 5 abas
gnome-terminal --window --maximize \
  --tab --title="1. SOAP (Docker)" -- bash -c "echo '🐳 Iniciando Container SOAP...'; docker run --name soap-container -p 8000:8000 -it soap-frete; exec bash" \
  --tab --title="2. Django" -- bash -c "cd '$BASE_DIR/src/api-catalogo-django'; source venv/bin/activate; echo '🐍 Iniciando Django...'; python manage.py runserver 0.0.0.0:8001; exec bash" \
  --tab --title="3. Express" -- bash -c "cd '$BASE_DIR/src/api-logistica-express'; echo '🟢 Iniciando Node...'; node server.js; exec bash" \
  --tab --title="4. Gateway" -- bash -c "cd '$BASE_DIR/src/api-gateway-fastapi'; source venv/bin/activate; echo '⚡ Iniciando Gateway...'; uvicorn main:app --host 0.0.0.0 --port 8080 --reload; exec bash" \
  --tab --title="5. Vue" -- bash -c "cd '$BASE_DIR/src/loja-vue'; echo '💻 Iniciando Vue...'; npm run dev; exec bash"

echo "✅ Todos os serviços foram solicitados!"