const dgram = require('dgram');
const net = require('net');
const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http, { 
    cors: { origin: "*" }, // Permite que o celular conecte
    maxHttpBufferSize: 1e8 // Permite fotos grandes
});

// ==========================================
// CONFIGURAÇÃO DE REDE
// ==========================================
const SEU_IP_PC = '192.168.0.238'; // <--- COLOQUE O SEU IP AQUI !!!
const PORTA_UDP = 4000;
const PORTA_TCP = 5000;

// ==========================================
// 1. OUVINTE UDP (Recebe o texto da rede)
// ==========================================
const udpSocket = dgram.createSocket('udp4');

udpSocket.on('listening', () => {
    udpSocket.setBroadcast(true); // Permite falar com a rede toda
    console.log(`📡 UDP ouvindo na porta ${PORTA_UDP}`);
});

udpSocket.on('message', (msg, rinfo) => {
    // Quando um pacote UDP chega, avisa todos os Frontends
    const raw = msg.toString();
    let text, nome;
    
    try {
        // Novo formato JSON do cliente P2P
        const data = JSON.parse(raw);
        text = data.texto;
        nome = data.nome;
    } catch {
        // Formato texto simples (compatibilidade)
        text = raw;
        nome = null;
    }
    
    console.log(`[UDP ← ${rinfo.address}:${rinfo.port}] ${nome ? `(${nome}) ` : ''}"${text}"`);
    io.emit('new-message', { 
        type: 'text', 
        content: nome ? `${nome}: ${text}` : text, 
        protocol: 'UDP', 
        from: rinfo.address,
        nome: nome
    });
});

// Ouve em TODAS as interfaces de rede (0.0.0.0)
udpSocket.bind(PORTA_UDP, '0.0.0.0');


// ==========================================
// 2. OUVINTE TCP (Recebe a foto da rede)
// ==========================================
const tcpServer = net.createServer((socket) => {
    let buffer = '';
    const clientAddr = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`[TCP ← ${clientAddr}] Nova conexão`);

    socket.on('data', (chunk) => {
        buffer += chunk.toString();
    });

    socket.on('end', () => {
        console.log(`[TCP ← ${clientAddr}] Arquivo recebido (${(buffer.length / 1024).toFixed(2)} KB)`);
        io.emit('new-message', { type: 'image', content: buffer, protocol: 'TCP', from: socket.remoteAddress });
    });
});

tcpServer.listen(PORTA_TCP, '0.0.0.0', () => {
    console.log(`📸 TCP ouvindo na porta ${PORTA_TCP}`);
});


// ==========================================
// 3. A PONTE (WebSocket -> Rede Real)
// ==========================================
io.on('connection', (socket) => {
    console.log(`📱 Novo dispositivo conectado: ${socket.id}`);

    // Quando o celular manda Texto...
    socket.on('send-text', (text) => {
        const message = Buffer.from(text);
        const client = dgram.createSocket('udp4');
        
        // ENVIA UM BROADCAST NA REDE
        // 255.255.255.255 significa "para todo mundo no wifi"
        client.bind(() => {
            client.setBroadcast(true);
            client.send(message, PORTA_UDP, '255.255.255.255', (err) => {
                client.close();
            });
        });
    });

    // Quando o celular manda Foto...
    socket.on('send-image', (base64Image) => {
        const client = new net.Socket();
        
        // CONECTA VIA TCP NO SEU PC
        // O dado sai do celular (WS), chega no Node, e o Node
        // abre uma conexão TCP real para a porta 5000 deste PC.
        client.connect(PORTA_TCP, SEU_IP_PC, () => {
            client.write(base64Image);
            client.end();
        });
    });
});

// Inicia o servidor HTTP para o Socket.io
http.listen(3000, '0.0.0.0', () => {
    console.log(`🚀 Backend rodando! Acesse no celular: http://${SEU_IP_PC}:5173`); // (Se o front estiver na 5173)
});