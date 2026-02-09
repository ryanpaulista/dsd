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

---

## 🔍 Explicação Detalhada do Código

### 1. Arquivo .proto (Contrato)

O arquivo `chat.proto` é o **coração do gRPC** - define o contrato que cliente e servidor devem seguir:

```protobuf
syntax = "proto3";    // Versão do Protocol Buffers
package chat;         // Namespace para evitar conflitos

// Estrutura de dados - similar a uma struct/class
message ChatMessage {
    string usuario = 1;    // Campo 1: nome do usuário
    string texto = 2;      // Campo 2: conteúdo da mensagem
    int64 timestamp = 3;   // Campo 3: momento do envio (ms)
}
// Os números (1, 2, 3) são identificadores únicos do campo no binário

// Definição do serviço - quais métodos o servidor expõe
service ChatService {
    // Unary: 1 request → 1 response
    rpc EnviarMensagem(ChatMessage) returns (ServerResponse);
    
    // Server Streaming: 1 request → N responses (stream)
    rpc ReceberMensagens(EntrarRequest) returns (stream ChatMessage);
    
    // Bidirectional: N requests ↔ N responses
    rpc ChatStream(stream ChatMessage) returns (stream ChatMessage);
}
```

**Por que usar .proto?**
- Tipagem forte em tempo de compilação
- Serialização binária ~10x mais rápida que JSON
- Gera código automaticamente para qualquer linguagem

---

### 2. Servidor Python (server.py)

#### 2.1 Importações e Setup

```python
import grpc
from concurrent import futures          # ThreadPool para múltiplos clientes
import chat_pb2                          # Mensagens geradas do .proto
import chat_pb2_grpc                     # Serviço gerado do .proto

mensagens = deque(maxlen=100)           # Histórico das últimas 100 msgs
listeners = []                           # Lista de clientes conectados
lock = threading.Lock()                  # Evita race conditions
```

#### 2.2 Implementando o Serviço

```python
class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    """Herda da classe abstrata gerada pelo protoc"""
    
    def EnviarMensagem(self, request, context):
        """
        RPC Unary - Recebe UMA mensagem, retorna UMA resposta
        
        - request: objeto ChatMessage com usuario, texto, timestamp
        - context: metadados da conexão (IP, headers, etc)
        """
        print(f"[MENSAGEM] {request.usuario}: {request.texto}")
        
        # Distribui para todos os clientes conectados
        with lock:
            for listener_queue in listeners:
                listener_queue.append(request)
        
        # Retorna resposta de sucesso
        return chat_pb2.ServerResponse(sucesso=True, mensagem="OK")
```

#### 2.3 Server Streaming (Receber Mensagens)

```python
def ReceberMensagens(self, request, context):
    """
    RPC Server Streaming - Cliente faz 1 request, servidor envia N mensagens
    
    O 'yield' transforma isso em um generator que envia mensagens
    continuamente enquanto o cliente estiver conectado.
    """
    queue = deque()              # Fila exclusiva deste cliente
    listeners.append(queue)      # Registra na lista global
    
    try:
        while context.is_active():       # Enquanto conexão ativa
            if queue:
                msg = queue.popleft()
                yield msg                # ← ENVIA mensagem via stream
            else:
                time.sleep(0.1)          # Evita CPU 100%
    finally:
        listeners.remove(queue)          # Limpa ao desconectar
```

#### 2.4 Iniciando o Servidor

```python
def serve():
    # Cria servidor com pool de 10 threads (10 clientes simultâneos)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Registra nossa implementação no servidor
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    
    # Escuta em todas interfaces na porta 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

---

### 3. Cliente Node.js (client.js)

#### 3.1 Carregando o .proto

```javascript
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

// Carrega o .proto em RUNTIME (não precisa gerar código antes)
const PROTO_PATH = path.join(__dirname, '../proto/chat.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,      // Mantém snake_case do proto
    longs: String,       // int64 → string (evita overflow JS)
    defaults: true       // Campos não enviados = valor padrão
});

// Extrai o serviço do pacote 'chat'
const chatProto = grpc.loadPackageDefinition(packageDefinition).chat;
```

#### 3.2 Criando o Cliente (Stub)

```javascript
// O "stub" é um proxy que faz as chamadas remotas parecerem locais
const client = new chatProto.ChatService(
    'localhost:50051',                    // Endereço do servidor
    grpc.credentials.createInsecure()     // Sem TLS (desenvolvimento)
);
```

#### 3.3 Recebendo Stream de Mensagens

```javascript
// Inicia Server Streaming - servidor vai enviar mensagens continuamente
const receberStream = client.ReceberMensagens({ usuario: USUARIO });

receberStream.on('data', (msg) => {
    // Evento disparado CADA VEZ que uma mensagem chega
    console.log(`[${msg.usuario}] ${msg.texto}`);
});

receberStream.on('error', (err) => {
    console.error('Erro:', err.message);
});

receberStream.on('end', () => {
    console.log('Servidor encerrou a conexão');
});
```

#### 3.4 Enviando Mensagens (Unary RPC)

```javascript
const mensagem = {
    usuario: USUARIO,
    texto: "Olá!",
    timestamp: Date.now()
};

// Chamada RPC assíncrona com callback
client.EnviarMensagem(mensagem, (err, response) => {
    if (err) {
        console.error('Falhou:', err.message);
    } else {
        console.log('Enviado:', response.mensagem);
    }
});
```

---

### 4. Fluxo Completo de uma Mensagem

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Cliente Node.js digita "Olá!"                                 │
├──────────────────────────────────────────────────────────────────┤
│ 2. client.EnviarMensagem() serializa para Protobuf binário       │
│    { usuario: "Alice", texto: "Olá!" } → [bytes compactos]       │
├──────────────────────────────────────────────────────────────────┤
│ 3. Envia via HTTP/2 para servidor Python :50051                  │
├──────────────────────────────────────────────────────────────────┤
│ 4. Servidor deserializa Protobuf → objeto Python                 │
│    chat_pb2.ChatMessage(usuario="Alice", texto="Olá!")           │
├──────────────────────────────────────────────────────────────────┤
│ 5. Servidor adiciona na queue de TODOS os listeners              │
├──────────────────────────────────────────────────────────────────┤
│ 6. ReceberMensagens() faz yield → envia via stream               │
├──────────────────────────────────────────────────────────────────┤
│ 7. Cliente Python/Node recebe no evento 'data'                   │
└──────────────────────────────────────────────────────────────────┘
```

---

### 5. Comparação: Por que gRPC e não REST?

| Cenário | REST | gRPC |
|---------|------|------|
| Chat em tempo real | Polling a cada 1s (ineficiente) | Stream contínuo HTTP/2 |
| Enviar 1000 msgs/s | JSON grande, lento | Protobuf binário, 10x menor |
| Múltiplas linguagens | Cada uma parseia JSON diferente | Contrato .proto gera código igual |
| Documentação | Swagger/OpenAPI opcional | .proto É a documentação |
