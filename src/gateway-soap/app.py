from flask import Flask
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_sock import Sock
import requests

class CORSMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Access-Control-Allow-Origin', '*'))
            headers.append(('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT, DELETE'))
            headers.append(('Access-Control-Allow-Headers', 'Content-Type, SOAPAction'))
            return start_response(status, headers, exc_info)

        if environ.get('REQUEST_METHOD') == 'OPTIONS':
            start_response('200 OK', [
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'POST, GET, OPTIONS'),
                ('Access-Control-Allow-Headers', 'Content-Type, SOAPAction')
            ])
            return [b'']

        return self.app(environ, custom_start_response)

app = Flask(__name__)
sock = Sock(app)

@sock.route('/ws')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(f"Gateway diz: Recebi '{data}'")

class Link(ComplexModel):
    rel = Unicode
    href = Unicode
    type = Unicode

class PedidoResponse(ComplexModel):
    id = Integer
    item = Unicode
    status = Unicode
    links = Iterable(Link)

class PedidoService(ServiceBase):
    @rpc(Integer, _returns=PedidoResponse)
    def consultar_pedido(ctx, pedido_id):
        # Busca API Python (Pedidos)
        try:
            resp_pedidos = requests.get(f'http://localhost:8001/pedidos/{pedido_id}')
            dados_pedido = resp_pedidos.json() if resp_pedidos.status_code == 200 else {"id": pedido_id, "item": "Não encontrado", "valor": 0}
        except:
            dados_pedido = {"id": pedido_id, "item": "Erro API Python", "valor": 0}

        # Busca API Node (Logística)
        try:
            resp_logistica = requests.get(f'http://localhost:8002/rastreio/{pedido_id}')
            dados_logistica = resp_logistica.json() if resp_logistica.status_code == 200 else {"status": "Desconhecido"}
        except:
            dados_logistica = {"status": "Erro API Node"}

        # HATEOAS
        links_hateoas = [
            Link(rel="self", href=f"http://localhost:8000/soap?wsdl", type="SOAP"),
            Link(rel="rastreio", href=f"http://localhost:8002/rastreio/{pedido_id}", type="REST_NODE"),
            Link(rel="stream", href="ws://localhost:8000/ws", type="WebSocket")
        ]

        return PedidoResponse(
            id=dados_pedido['id'],
            item=dados_pedido['item'],
            status=dados_logistica.get("status", "Indefinido"),
            links=links_hateoas
        )

soap_app = Application([PedidoService], 'tcc.soap.gateway',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

wsgi_app = WsgiApplication(soap_app)

# Junta Flask + Spyne
combined_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap': wsgi_app
})

app.wsgi_app = CORSMiddleware(combined_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)