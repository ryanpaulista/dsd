from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from service import FreteService

def create_app():
    app = Application(
        [FreteService], # serviços disponíveis
        'tns.brainz.frete', # 
        in_protocol=Soap11(validator='lxml'), # lxml garante que o XML não tenha erros de sintaxe
        out_protocol=Soap11()
    )

    return WsgiApplication(app)

if __name__ == '__main__':
    wsgi_app = create_app()
    host = '0.0.0.0'
    port = 8000

    print(f"==========================================")
    print(f" Servidor SOAP (Spyne) rodando")
    print(f" WSDL: http://127.0.0.1:{port}/?wsdl")
    print(f"==========================================")
    
    server = make_server(host, port, wsgi_app)
    server.serve_forever()