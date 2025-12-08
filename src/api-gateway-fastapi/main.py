from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from websocket_manager import manager
import aio_pika
import asyncio
import json
from config import settings
from routers import catalogo, logistica, compras

RABBITMQ_URL = settings.RABBITMQ_URL

async def consumir_notificacoes(app: FastAPI):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("fila_notificacoes", durable=True)

    print("[FILA_NOTIFICACOES] Gateway ouvindo fila_notificações")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                dados = message.body.decode()
                print(f"Evento recebido do Django: {dados}")
                await manager.broadcast(dados)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Conectando ao RabbitMQ")
    connection = None
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        channel = await connection.channel()

        await channel.declare_queue("fila_pedidos", durable=True) # Garante que a fila existe
        app.state.rabbitmq_connection = connection  
        app.state.rabbitmq_channel = channel

        task = asyncio.create_task(consumir_notificacoes(app)) # A tarefa paralela é criada que fica escutando a fila_notificações

        print("RabbitMQ pronto")
        yield
    except Exception as e:
        print(f"Erro no RabbitMQ: {e}")
        yield
    finally:
        if connection:
            await connection.close()
            task.cancel()
            print("RabbitMQ desconectado!")

app = FastAPI(
    lifespan=lifespan,
    title="Brainz E-Shop Gateway",
    description="Gateway central com HATEOAS.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalogo.router)
app.include_router(logistica.router)
app.include_router(compras.router)

@app.get("/", tags=["Status"])
async def root():
    return {"status": "Gateway Online", "docs": "/docs"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)