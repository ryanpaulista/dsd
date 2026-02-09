#!/bin/bash
#
# Script de teste - Demonstra uso real de TCP/UDP
#

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🧪 Teste de Protocolos TCP/UDP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verifica se o servidor está rodando
if ! nc -z localhost 4000 2>/dev/null; then
    echo "⚠️  Servidor não está rodando!"
    echo "   Execute: npm start"
    exit 1
fi

echo "✅ Servidor detectado"
echo ""

# Teste UDP
echo "📡 Enviando mensagem via UDP..."
node udp-client.js "Teste UDP - $(date +%H:%M:%S)"
sleep 1

# Cria uma imagem de teste se não existir
if [ ! -f "test-image.png" ]; then
    echo "📸 Criando imagem de teste..."
    # Cria um pequeno PNG (1x1 pixel vermelho)
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==" | base64 -d > test-image.png
fi

echo "📸 Enviando imagem via TCP..."
node tcp-client.js 127.0.0.1 test-image.png

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Testes concluídos!"
echo "  Verifique os logs do servidor."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
