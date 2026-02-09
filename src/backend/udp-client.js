#!/usr/bin/env node
const dgram = require('dgram');
const readline = require('readline');
const os = require('os');

const PORTA_UDP = 4000;
const BROADCAST_ADDR = '255.255.255.255';

const NOME = process.argv[2] || os.hostname();

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

const socket = dgram.createSocket({ type: 'udp4', reuseAddr: true });

socket.bind(PORTA_UDP, '0.0.0.0', () => {
    socket.setBroadcast(true);
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('  📡 Chat UDP P2P via Broadcast');
    console.log(`  Nome: ${NOME}`);
    console.log(`  IP: ${MEU_IP}`);
    console.log(`  Porta: ${PORTA_UDP}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('  Qualquer PC na rede pode enviar/receber!');
    console.log('  Digite suas mensagens abaixo:\n');
});

socket.on('message', (msg, rinfo) => {
    try {
        const data = JSON.parse(msg.toString());
        if (data.nome === NOME) return;
        
        console.log(`\n[${data.nome}@${rinfo.address}] ${data.texto}`);
        process.stdout.write('> ');
    } catch {
        console.log(`\n[${rinfo.address}] ${msg.toString()}`);
        process.stdout.write('> ');
    }
});

function enviarMensagem(texto) {
    const data = JSON.stringify({ nome: NOME, texto: texto });
    const message = Buffer.from(data);
    
    socket.send(message, PORTA_UDP, BROADCAST_ADDR, (err) => {
        if (err) {
            console.error('[ERRO]', err.message);
        }
    });
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: '> '
});

rl.prompt();

rl.on('line', (input) => {
    if (input.trim()) {
        enviarMensagem(input.trim());
        console.log(`[Você] ${input.trim()}`);
    }
    rl.prompt();
});

rl.on('close', () => {
    console.log('\n👋 Saindo do chat UDP...');
    socket.close();
    process.exit(0);
});

socket.on('error', (err) => {
    console.error('[ERRO SOCKET]', err.message);
    process.exit(1);
});
