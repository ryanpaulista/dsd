# TCC - API Gateway SOAP & WebSocket

Este projeto demonstra uma arquitetura de microsserviços utilizando um API Gateway SOAP com implementação de HATEOAS e comunicação em tempo real via WebSocket.

## 🏛 Arquitetura

1. **Gateway (Porta 8000):** Python + Spyne (SOAP) + Flask.
2. **Serviço de Pedidos (Porta 8001):** Python Flask (REST).
3. **Serviço de Logística (Porta 8002):** Node.js Express (REST).
4. **Frontend:** Vue.js + Vite.

## 🚀 Como Rodar

### 1. Backend (Gateway e Microsserviços)
É necessário abrir 3 terminais:

```bash
# Terminal 1: Gateway
cd gateway-soap
source venv/bin/activate
python app.py

# Terminal 2: API Pedidos
cd api-pedidos-python
source venv/bin/activate
python app.py

# Terminal 3: API Logística
cd api-logistica-node
npm start (ou node server.js)
```

### 2. Frontend (Cliente Web)
```bash
cd client-vue
npm run dev
```
Acesse: `http://localhost:5173`