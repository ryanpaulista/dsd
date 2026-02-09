#!/usr/bin/env python3
"""
Cliente gRPC de Chat - Python
Conecta ao servidor na porta 50051
"""

import grpc
import threading
import sys
import time

# Importa os módulos gerados pelo protoc
import chat_pb2
import chat_pb2_grpc


def receber_mensagens(stub, usuario):
    """Thread para receber mensagens do servidor"""
    try:
        request = chat_pb2.EntrarRequest(usuario=usuario)
        for msg in stub.ReceberMensagens(request):
            timestamp = time.strftime('%H:%M:%S', time.localtime(msg.timestamp / 1000))
            print(f"\n[{timestamp}] {msg.usuario}: {msg.texto}")
            print("> ", end="", flush=True)
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.CANCELLED:
            print(f"\n[ERRO] {e.details()}")


def main():
    # Configuração
    server_addr = sys.argv[1] if len(sys.argv) > 1 else 'localhost:50051'
    usuario = sys.argv[2] if len(sys.argv) > 2 else f'Python_{id(object())}'
    
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('  🐍 Cliente gRPC de Chat - Python')
    print(f'  Servidor: {server_addr}')
    print(f'  Usuário: {usuario}')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('  Digite suas mensagens abaixo:\n')
    
    # Conecta ao servidor
    channel = grpc.insecure_channel(server_addr)
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    
    # Inicia thread para receber mensagens
    receiver = threading.Thread(target=receber_mensagens, args=(stub, usuario))
    receiver.daemon = True
    receiver.start()
    
    try:
        while True:
            texto = input("> ")
            if not texto.strip():
                continue
            
            # Envia a mensagem
            msg = chat_pb2.ChatMessage(
                usuario=usuario,
                texto=texto,
                timestamp=int(time.time() * 1000)
            )
            
            try:
                response = stub.EnviarMensagem(msg)
                print(f"[Você] {texto}")
            except grpc.RpcError as e:
                print(f"[ERRO] {e.details()}")
    
    except KeyboardInterrupt:
        print("\n👋 Saindo do chat...")
    finally:
        channel.close()


if __name__ == '__main__':
    main()
