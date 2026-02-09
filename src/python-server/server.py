#!/usr/bin/env python3
"""
Servidor gRPC de Chat - Python
Porta: 50051
"""

import grpc
from concurrent import futures
import time
import threading
from collections import deque

# Importa os módulos gerados pelo protoc
import chat_pb2
import chat_pb2_grpc

# Armazena as últimas mensagens e os listeners conectados
mensagens = deque(maxlen=100)
listeners = []  # Lista de queues para cada cliente conectado
lock = threading.Lock()


class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    """Implementação do serviço de chat"""

    def EnviarMensagem(self, request, context):
        """Recebe uma mensagem e distribui para todos os listeners"""
        print(f"[MENSAGEM] {request.usuario}: {request.texto}")
        
        # Adiciona timestamp se não tiver
        if request.timestamp == 0:
            request = chat_pb2.ChatMessage(
                usuario=request.usuario,
                texto=request.texto,
                timestamp=int(time.time() * 1000)
            )
        
        # Armazena a mensagem
        with lock:
            mensagens.append(request)
            # Notifica todos os listeners
            for listener_queue in listeners:
                listener_queue.append(request)
        
        return chat_pb2.ServerResponse(
            sucesso=True,
            mensagem=f"Mensagem enviada por {request.usuario}"
        )

    def ReceberMensagens(self, request, context):
        """Stream de mensagens para o cliente (Server Streaming)"""
        print(f"[CONECTADO] {request.usuario} entrou no chat")
        
        # Cria uma queue para este cliente
        queue = deque()
        with lock:
            listeners.append(queue)
        
        try:
            while context.is_active():
                # Verifica se há mensagens na queue
                if queue:
                    msg = queue.popleft()
                    # Não envia mensagens do próprio usuário
                    if msg.usuario != request.usuario:
                        yield msg
                else:
                    time.sleep(0.1)  # Evita busy waiting
        finally:
            with lock:
                if queue in listeners:
                    listeners.remove(queue)
            print(f"[DESCONECTADO] {request.usuario} saiu do chat")

    def ChatStream(self, request_iterator, context):
        """Chat bidirecional (Bidirectional Streaming)"""
        # Cria uma queue para este cliente
        queue = deque()
        usuario = None
        
        with lock:
            listeners.append(queue)
        
        def receber_mensagens():
            """Thread para receber mensagens do cliente"""
            nonlocal usuario
            try:
                for msg in request_iterator:
                    if usuario is None:
                        usuario = msg.usuario
                        print(f"[CONECTADO] {usuario} entrou no chat (bidirecional)")
                    
                    print(f"[MENSAGEM] {msg.usuario}: {msg.texto}")
                    
                    # Adiciona timestamp
                    msg_with_ts = chat_pb2.ChatMessage(
                        usuario=msg.usuario,
                        texto=msg.texto,
                        timestamp=int(time.time() * 1000)
                    )
                    
                    # Distribui para todos os listeners
                    with lock:
                        mensagens.append(msg_with_ts)
                        for listener_queue in listeners:
                            if listener_queue is not queue:  # Não envia para si mesmo
                                listener_queue.append(msg_with_ts)
            except Exception as e:
                print(f"[ERRO] Erro ao receber: {e}")
        
        # Inicia thread para receber mensagens
        receiver = threading.Thread(target=receber_mensagens)
        receiver.daemon = True
        receiver.start()
        
        try:
            while context.is_active():
                if queue:
                    msg = queue.popleft()
                    yield msg
                else:
                    time.sleep(0.1)
        finally:
            with lock:
                if queue in listeners:
                    listeners.remove(queue)
            if usuario:
                print(f"[DESCONECTADO] {usuario} saiu do chat")


import socket

def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def serve():
    """Inicia o servidor gRPC"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    
    porta = 50051
    ip_local = get_local_ip()
    
    server.add_insecure_port(f'0.0.0.0:{porta}')
    server.start()
    
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('  🐍 Servidor gRPC de Chat - Python')
    print(f'  IP: {ip_local}')
    print(f'  Porta: {porta}')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print(f'  Conecte com: {ip_local}:{porta}')
    print('  Aguardando conexões...\n')
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('\n👋 Servidor encerrado.')
        server.stop(0)


if __name__ == '__main__':
    serve()
