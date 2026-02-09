# Chat gRPC - Python + Node.js

Sistema de chat em tempo real utilizando **gRPC** com duas linguagens diferentes:
- **Servidor:** Python
- **Cliente:** Node.js (e também Python)

## 🏛 Arquitetura

```
┌─────────────────────┐         ┌─────────────────────┐
│   Cliente Node.js   │  gRPC   │                     │
│    (client.js)      │ ──────► │                     │
└─────────────────────┘  :50051 │   Servidor Python   │
                                │    (server.py)      │
┌─────────────────────┐         │                     │
│   Cliente Python    │  gRPC   │   0.0.0.0:50051     │
│    (client.py)      │ ──────► │                     │
└─────────────────────┘         └─────────────────────┘
```

## 📚 O que é gRPC?

**gRPC** (Google Remote Procedure Call) é um framework de comunicação entre serviços que usa:

- **Protocol Buffers (Protobuf)** para serialização de dados (binário, mais rápido que JSON)
- **HTTP/2** para transporte (multiplexação, streaming)
- **Arquivo .proto** como contrato obrigatório entre cliente e servidor

### Diferenças: gRPC vs REST

| Aspecto | REST | gRPC |
|---------|------|------|
| Formato | JSON (texto) | Protobuf (binário) |
| Velocidade | Mais lento | ~10x mais rápido |
| Contrato | OpenAPI (opcional) | **.proto (obrigatório)** |
| Streaming | Workarounds | Nativo |

### Tipos de RPC

```
1. Unary (simples)
   Cliente ──[msg]──► Servidor ──[resp]──► Cliente

2. Server Streaming  
   Cliente ──[req]──► Servidor ══[msg1]══[msg2]══► Cliente

3. Bidirectional Streaming
   Cliente ══[msg]══► ◄══[msg]══ Servidor
```

## 📁 Estrutura do Projeto

```
src/
├── proto/
│   └── chat.proto          # Contrato gRPC (obrigatório)
├── python-server/
│   ├── server.py           # Servidor gRPC (Python)
│   ├── client.py           # Cliente de teste (Python)
│   ├── chat_pb2.py         # Gerado pelo protoc
│   ├── chat_pb2_grpc.py    # Gerado pelo protoc
│   ├── requirements.txt    # Dependências Python
│   └── generate.sh         # Script para gerar código
└── node-client/
    ├── client.js           # Cliente gRPC (Node.js)
    └── package.json        # Dependências Node.js
```

## 🚀 Como Executar

### 1. Servidor Python

```bash
cd src/python-server

# Criar ambiente virtual e ativar
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip setuptools
pip install -r requirements.txt

# Gerar código do .proto
./generate.sh

# Iniciar o servidor
python server.py
```

Saída esperada:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🐍 Servidor gRPC de Chat - Python
  IP: 192.168.0.238
  Porta: 50051
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Conecte com: 192.168.0.238:50051
  Aguardando conexões...
```

### 2. Cliente Node.js

```bash
cd src/node-client

# Instalar dependências
npm install

# Conectar ao servidor (use o IP mostrado pelo servidor)
node client.js 192.168.0.238:50051 "SeuNome"
```

### 3. Cliente Python (alternativo)

```bash
cd src/python-server
source venv/bin/activate

python client.py 192.168.0.238:50051 "OutroNome"
```

## 📝 Exemplo de Uso

**Servidor:**
```
[CONECTADO] Alice entrou no chat
[MENSAGEM] Alice: Olá pessoal!
[CONECTADO] Bob entrou no chat
[MENSAGEM] Bob: Oi Alice!
```

**Cliente Node.js (Alice):**
```
> Olá pessoal!
[Você] Olá pessoal!

[14:30:25] Bob: Oi Alice!
```

**Cliente Python (Bob):**
```
> Oi Alice!
[Você] Oi Alice!
```

## 🔧 Métodos gRPC Implementados

| Tipo | Método | Descrição |
|------|--------|-----------|
| **Unary** | `EnviarMensagem` | Envia uma mensagem |
| **Server Streaming** | `ReceberMensagens` | Recebe stream de mensagens |
| **Bidirectional** | `ChatStream` | Chat em tempo real |

## 📡 Contrato gRPC (chat.proto)

```protobuf
syntax = "proto3";
package chat;

message ChatMessage {
    string usuario = 1;
    string texto = 2;
    int64 timestamp = 3;
}

service ChatService {
    rpc EnviarMensagem(ChatMessage) returns (ServerResponse);
    rpc ReceberMensagens(EntrarRequest) returns (stream ChatMessage);
    rpc ChatStream(stream ChatMessage) returns (stream ChatMessage);
}
```

## 🔗 Como o .proto conecta as linguagens

```
chat.proto ──► protoc ──► chat_pb2.py (Python)
                     └──► Carregado em runtime (Node.js)
                     
Python usa: import chat_pb2
Node.js usa: protoLoader.loadSync('chat.proto')

Ambos "falam a mesma língua" graças ao contrato .proto
```
