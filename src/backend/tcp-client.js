#!/usr/bin/env node
/**
 * Cliente TCP - Envia E recebe arquivos via TCP
 * 
 * Fica escutando conexões E pode enviar para outros IPs.
 * 
 * Uso: node tcp-client.js [nome] [porta]
 *      Depois digite: enviar IP:PORTA arquivo.jpg
 *      Exemplo: enviar 127.0.0.1:5001 foto.jpg
 */

const net = require('net');
const fs = require('fs');
const path = require('path');
const readline = require('readline');
const os = require('os');

// Configuração
const NOME = process.argv[2] || os.hostname();
const PORTA_TCP = parseInt(process.argv[3]) || 5000;

// Obtém IP local
function getLocalIP() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    return '127.0.0.1';
}

const MEU_IP = getLocalIP();

const PASTA_RECEBIDOS = './recebidos';
if (!fs.existsSync(PASTA_RECEBIDOS)) {
    fs.mkdirSync(PASTA_RECEBIDOS);
}

const server = net.createServer((socket) => {
    let buffer = Buffer.alloc(0);
    const clientAddr = `${socket.remoteAddress.replace('::ffff:', '')}`;
    
    console.log(`\n[TCP ← ${clientAddr}] Recebendo arquivo...`);

    socket.on('data', (chunk) => {
        buffer = Buffer.concat([buffer, chunk]);
    });

    socket.on('end', () => {
        const timestamp = Date.now();
        const nomeArquivo = `${PASTA_RECEBIDOS}/arquivo_${timestamp}`;
        
        // Verifica se é base64 de imagem
        const dataStr = buffer.toString();
        if (dataStr.startsWith('data:image')) {
            const matches = dataStr.match(/^data:image\/(\w+);base64,(.+)$/);
            if (matches) {
                const ext = matches[1] === 'jpeg' ? 'jpg' : matches[1];
                const base64Data = matches[2];
                const filePath = `${nomeArquivo}.${ext}`;
                fs.writeFileSync(filePath, Buffer.from(base64Data, 'base64'));
                console.log(`[TCP ✓] Imagem salva: ${filePath} (${(buffer.length / 1024).toFixed(2)} KB)`);
            }
        } else {
            // Salva como arquivo genérico
            const filePath = `${nomeArquivo}.bin`;
            fs.writeFileSync(filePath, buffer);
            console.log(`[TCP ✓] Arquivo salvo: ${filePath} (${(buffer.length / 1024).toFixed(2)} KB)`);
        }
        process.stdout.write('> ');
    });

    socket.on('error', (err) => {
        console.error(`[TCP ERRO] ${err.message}`);
    });
});

server.listen(PORTA_TCP, '0.0.0.0', () => {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('  📸 Cliente TCP P2P - Arquivos');
    console.log(`  Nome: ${NOME}`);
    console.log(`  IP: ${MEU_IP}`);
    console.log(`  Porta: ${PORTA_TCP}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('  Comandos:');
    console.log('    enviar <IP:PORTA> <arquivo>');
    console.log('    Exemplo: enviar 127.0.0.1:5001 foto.jpg');
    console.log('');
    console.log('  Arquivos recebidos salvos em: ./recebidos/\n');
});

function enviarArquivo(destino, caminhoArquivo) {
    if (!fs.existsSync(caminhoArquivo)) {
        console.error(`[ERRO] Arquivo não encontrado: ${caminhoArquivo}`);
        return;
    }

    // Suporta IP:PORTA ou só IP (usa porta padrão 5000)
    let ip, porta;
    if (destino.includes(':')) {
        [ip, porta] = destino.split(':');
        porta = parseInt(porta);
    } else {
        ip = destino;
        porta = 5000;
    }

    const fileBuffer = fs.readFileSync(caminhoArquivo);
    const ext = path.extname(caminhoArquivo).toLowerCase().slice(1);
    const mimeType = getMimeType(ext);
    const base64Data = `data:${mimeType};base64,${fileBuffer.toString('base64')}`;

    const client = new net.Socket();
    
    console.log(`[TCP →] Conectando a ${ip}:${porta}...`);

    client.connect(porta, ip, () => {
        console.log(`[TCP →] Enviando ${path.basename(caminhoArquivo)} (${(fileBuffer.length / 1024).toFixed(2)} KB)...`);
        client.write(base64Data);
        client.end();
    });

    client.on('close', () => {
        console.log(`[TCP ✓] Arquivo enviado para ${ip}:${porta}!`);
        process.stdout.write('> ');
    });

    client.on('error', (err) => {
        console.error(`[TCP ERRO] ${err.message}`);
        process.stdout.write('> ');
    });
}

function getMimeType(ext) {
    const mimeTypes = {
        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
        'png': 'image/png', 'gif': 'image/gif',
        'webp': 'image/webp', 'bmp': 'image/bmp',
        'txt': 'text/plain', 'pdf': 'application/pdf'
    };
    return mimeTypes[ext] || 'application/octet-stream';
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: '> '
});

rl.prompt();

rl.on('line', (input) => {
    const args = input.trim().split(/\s+/);
    const cmd = args[0]?.toLowerCase();
    
    if (cmd === 'enviar' && args[1] && args[2]) {
        enviarArquivo(args[1], args[2]);
    } else if (cmd === 'ajuda' || cmd === 'help') {
        console.log('Comandos: enviar <IP> <arquivo>');
    } else if (input.trim()) {
        console.log('Comando inválido. Use: enviar <IP> <arquivo>');
        rl.prompt();
    } else {
        rl.prompt();
    }
});

rl.on('close', () => {
    console.log('\n👋 Saindo do cliente TCP...');
    server.close();
    process.exit(0);
});

server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`[ERRO] Porta ${PORTA_TCP} já em uso. Outro cliente TCP rodando?`);
    } else {
        console.error('[ERRO]', err.message);
    }
    process.exit(1);
});
