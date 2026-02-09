# Chat P2P com TCP/UDP

Sistema de comunicação peer-to-peer utilizando protocolos TCP e UDP puros.

## Arquitetura P2P

```
┌─────────────────┐  UDP Broadcast   ┌─────────────────┐
│   Computador A  │ ◄──────────────► │   Computador B  │
│  udp-client.js  │     porta 4000   │  udp-client.js  │
│  tcp-client.js  │ ◄──────────────► │  tcp-client.js  │
└─────────────────┘  TCP porta 5000  └─────────────────┘
```

## Portas Utilizadas

| Protocolo | Porta | Uso |
|-----------|-------|-----|
| **UDP**   | 4000  | Chat de texto via broadcast |
| **TCP**   | 5000+ | Transferência de arquivos P2P |

## 🚀 Como Executar o Chat UDP (Texto)

O UDP usa broadcast - todos na rede recebem automaticamente.

```bash
# Terminal 1
cd src/backend
node udp-client.js "Alice"

# Terminal 2 (mesma máquina ou outro PC na rede)
cd src/backend
node udp-client.js "Bob"
```

Digite mensagens em qualquer terminal - todos recebem via broadcast UDP.

## 🚀 Como Executar o Chat TCP (Arquivos)

O TCP é ponto-a-ponto - você escolhe para quem enviar.

```bash
# Terminal 1 - escuta na porta 5000
cd src/backend
node tcp-client.js "Alice" 5000

# Terminal 2 - escuta na porta 5001 (mesma máquina)
cd src/backend
node tcp-client.js "Bob" 5001
```

Para enviar um arquivo:
```
> enviar 127.0.0.1:5000 /caminho/para/arquivo.jpg
```

## 📝 Exemplos de Uso

**UDP - Enviar mensagem de texto:**
```
> Olá, tudo bem?
[Você] Olá, tudo bem?
```

**TCP - Enviar arquivo para outro PC:**
```
> enviar 192.168.0.100:5000 ~/Downloads/foto.jpg
[TCP →] Conectando a 192.168.0.100:5000...
[TCP →] Enviando foto.jpg (125.50 KB)...
[TCP ✓] Arquivo enviado para 192.168.0.100:5000!
```

## 🔓 Liberando Firewall (se necessário)

```bash
sudo ufw allow 4000/udp
sudo ufw allow 5000/tcp
sudo ufw allow 5001/tcp
```

## 📁 Arquivos Recebidos

Arquivos recebidos via TCP são salvos em:
```
src/backend/recebidos/
```
