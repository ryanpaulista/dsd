# Chat TCP/UDP - P2P

Sistema de chat **peer-to-peer** que demonstra o uso **real** dos protocolos TCP e UDP.

## Arquitetura P2P

```
┌─────────────────┐  UDP Broadcast   ┌─────────────────┐
│   Computador A  │ ◄──────────────► │   Computador B  │
│  udp-client.js  │     porta 4000   │  udp-client.js  │
│  tcp-client.js  │ ◄──────────────► │  tcp-client.js  │
└─────────────────┘  TCP porta 5000  └─────────────────┘
         │                                    │
         └──────────────┬─────────────────────┘
                        ▼
              ┌─────────────────┐
              │    Servidor     │  (opcional, para visualização web)
              │   (server.js)   │
              │    WebSocket    │
              └─────────────────┘
                        │
              ┌─────────────────┐
              │    Frontend     │
              │    (Vue.js)     │
              └─────────────────┘
```

## Portas Utilizadas

| Protocolo | Porta | Uso |
|-----------|-------|-----|
| **UDP**   | 4000  | Chat de texto via broadcast (todos recebem) |
| **TCP**   | 5000  | Transferência de arquivos P2P (conexão direta) |
| WebSocket | 3000  | Interface web para visualização (opcional) |

## Como Usar - Chat P2P

### 1. Chat de Texto via UDP (Broadcast)

Qualquer computador na rede pode enviar E receber mensagens!

```bash
# Em cada computador da rede:
cd src/backend
node udp-client.js "SeuNome"
```

Depois é só digitar mensagens - todos na rede vão receber automaticamente.

### 2. Envio de Arquivos via TCP

Cada computador pode enviar E receber arquivos:

```bash
# Em cada computador da rede:
cd src/backend
node tcp-client.js "SeuNome"

# Para enviar arquivo para outro PC:
> enviar 192.168.0.100 foto.jpg
```

Arquivos recebidos são salvos em `./recebidos/`

### 3. Visualização Web (Opcional)

```bash
# Terminal 1 - Servidor
cd src/backend && npm start

# Terminal 2 - Frontend
cd src/frontend/dsd-project && npm run dev
```

## Demonstração dos Protocolos

### UDP - User Datagram Protocol
- **Broadcast**: Mensagem vai para TODOS os computadores na rede
- **Sem conexão**: Não precisa saber quem está ouvindo
- **Rápido**: Ideal para chat em tempo real
- **Escuta em 0.0.0.0**: Aceita pacotes de qualquer origem

### TCP - Transmission Control Protocol
- **Ponto a ponto**: Conexão direta entre dois computadores
- **Bidirecional**: Cada cliente também é servidor (P2P)
- **Confiável**: Garante que o arquivo chega completo
- **Orientado a conexão**: Handshake antes de transferir

## Testando na Mesma Rede

1. **Computador A** (192.168.0.10):
   ```bash
   node udp-client.js "Alice"
   node tcp-client.js
   ```

2. **Computador B** (192.168.0.20):
   ```bash
   node udp-client.js "Bob"
   node tcp-client.js
   ```

3. Alice digita "Olá!" → Bob recebe via UDP broadcast
4. Bob digita `enviar 192.168.0.10 foto.jpg` → Alice recebe via TCP

## Logs

```
[UDP ← 192.168.0.20:54321] (Bob) "Olá, Alice!"
[TCP ← 192.168.0.20] Recebendo arquivo...
[TCP ✓] Imagem salva: ./recebidos/arquivo_1707494400.jpg (125.50 KB)
```
