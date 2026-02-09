#!/usr/bin/env node
/**
 * Cliente gRPC de Chat - Node.js
 * Conecta ao servidor Python na porta 50051
 */

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const readline = require('readline');
const path = require('path');

// Carrega o arquivo .proto
const PROTO_PATH = path.join(__dirname, '../proto/chat.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const chatProto = grpc.loadPackageDefinition(packageDefinition).chat;

// Configuração
const SERVER_ADDR = process.argv[2] || '172.16.0.2:50051';
const USUARIO = process.argv[3] || `Node_${process.pid}`;

// Cria o cliente gRPC
const client = new chatProto.ChatService(
    SERVER_ADDR,
    grpc.credentials.createInsecure()
);

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  📦 Cliente gRPC de Chat - Node.js');
console.log(`  Servidor: ${SERVER_ADDR}`);
console.log(`  Usuário: ${USUARIO}`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  Digite suas mensagens abaixo:\n');

// Inicia o stream para receber mensagens
const receberStream = client.ReceberMensagens({ usuario: USUARIO });

receberStream.on('data', (msg) => {
    const time = new Date(parseInt(msg.timestamp)).toLocaleTimeString();
    console.log(`\n[${time}] ${msg.usuario}: ${msg.texto}`);
    process.stdout.write('> ');
});

receberStream.on('error', (err) => {
    if (err.code !== grpc.status.CANCELLED) {
        console.error('\n[ERRO]', err.message);
    }
});

receberStream.on('end', () => {
    console.log('\n[INFO] Conexão encerrada pelo servidor.');
    process.exit(0);
});

// Interface de linha de comando
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: '> '
});

rl.prompt();

rl.on('line', (input) => {
    const texto = input.trim();
    if (!texto) {
        rl.prompt();
        return;
    }

    // Envia a mensagem via gRPC
    const mensagem = {
        usuario: USUARIO,
        texto: texto,
        timestamp: Date.now()
    };

    client.EnviarMensagem(mensagem, (err, response) => {
        if (err) {
            console.error('[ERRO]', err.message);
        } else {
            console.log(`[Você] ${texto}`);
        }
        rl.prompt();
    });
});

rl.on('close', () => {
    console.log('\n👋 Saindo do chat...');
    receberStream.cancel();
    process.exit(0);
});

// Tratamento de sinais
process.on('SIGINT', () => {
    rl.close();
});
