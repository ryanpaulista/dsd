from fastapi import APIRouter, HTTPException, Request
from schemas import CompraRequest
import json
import aio_pika

router = APIRouter(tags=["Compra"])

@router.post("/comprar")
async def realizar_compra(request: Request, dados: CompraRequest):
    """
        Recebe o pedido de compra e adiciona a fila para processamento
    """
    try:
        channel = request.app.state.rabbitmq_channel

        mensagem = {
            "id_produto": dados.id_produto,
            "quantidade": dados.quantidade
        }

        await channel.default_exchange.publish( # Momento que a mensagem é publicada na fila.
            aio_pika.Message(
                body=json.dumps(mensagem).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key="fila_pedidos"
        )

        return {
            "mensagem": "Pedido recebido com sucesso. Vocẽ será notificado quando a compra for efetivada",
            "status": "processando",
        }
    except Exception as e:
        print(f"Erro ao publicar no RabbitMQ {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar pedido")