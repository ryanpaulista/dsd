#!/bin/bash

BASE_DIR=$(pwd)
echo "🚀 Iniciando Brainz E-Shop em janelas separadas..."

# Abre SOAP
gnome-terminal --title="1. SOAP" -- bash -c "cd '$BASE_DIR/src/soap-frete-service'; source venv/bin/activate; echo '🐍 SOAP Service'; python main.py; exec bash" &

# Abre Django - Processo Web 
sleep 1 # Pequena pausa para garantir ordem
gnome-terminal --title="2. Django" -- bash -c "cd '$BASE_DIR/src/api-catalogo-django'; source venv/bin/activate; echo '🐍 Django API'; python manage.py runserver 0.0.0.0:8001; exec bash" &

# Abre o Django - Processo Worker
gnome-terminal --title="2.1 Django" -- bash -c "cd '$BASE_DIR/src/api-catalogo-django'; source venv/bin/activate; echo '🐍 Django API-Worker'; python manage.py run_consumer; exec bash" &

# Abre Express
sleep 1
gnome-terminal --title="3. Express" -- bash -c "cd '$BASE_DIR/src/api-logistica-express'; echo '🟢 Node Express'; node server.js; exec bash" &

# Abre Gateway
sleep 1
gnome-terminal --title="4. Gateway" -- bash -c "cd '$BASE_DIR/src/api-gateway-fastapi'; source venv/bin/activate; echo '⚡ FastAPI Gateway'; uvicorn main:app --host 0.0.0.0 --port 8080 --reload; exec bash" &

# Abre Vue
sleep 1
gnome-terminal --title="5. Vue" -- bash -c "cd '$BASE_DIR/src/loja-vue'; echo '💻 Vue Frontend'; npm run dev; exec bash" &

echo "✅ Todas as janelas foram solicitadas!"