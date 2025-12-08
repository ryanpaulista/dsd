import json
import pika

from django.core.management.base import BaseCommand
from django.conf import settings
from ...services.compra_service import CompraService 

class Command(BaseCommand):
    help = 'Roda o consumidor de mensagens do RabbitMQ para processar pedidos'

    def handle(self, *args, **options):
        RABBITMQ_URL = settings.RABBITMQ_URL

        self.stdout.write(self.style.WARNING('Iniciando o consumidor Django...'))
        
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue='fila_pedidos', durable=True)

        def callback(ch, method, properties, body):
            try:
                dados = json.loads(body)

                self.stdout.write(self.style.SUCCESS(f"Novo pedido recebido: {dados}"))

                #LOGICA DE NEGOCIO - REGISTRO DE PEDIDO
                estoque = CompraService.registrar_compra(dados['id_produto'], dados['quantidade'])
                self.stdout.write(f"✅ Pedido salvo no Banco de Dados!")

                notificacao = {
                    "tipo": "ATUALIZACAO_ESTOQUE",
                    "id_produto": dados['id_produto'],
                    "novo_estoque": estoque,
                    "mensagem": f"Pedido de {dados['quantidade']} produto confirmado!"
                }

                ch.basic_publish( # Momento em que a notificação de retorno é publicada na fila.
                    exchange='',
                    routing_key='fila_notificacoes',
                    body=json.dumps(notificacao)
                )

                self.stdout.write(self.style.SUCCESS(f"📢 Notificação enviada para fila_notificacoes"))

                ch.basic_ack(delivery_tag=method.delivery_tag)
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao processar pedido {e}"))
            
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="fila_pedidos", on_message_callback=callback)
        
        self.stdout.write(self.style.SUCCESS("Aguardando mensagens da fila."))

        channel.start_consuming()
        
