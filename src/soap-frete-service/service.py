from spyne import ServiceBase, rpc, Unicode, Float
from models import FreteResponse

class FreteService(ServiceBase):
    @rpc(Unicode, Float, _returns=FreteResponse)
    def calcular_frete(ctx, cep, peso):
        """
            Lógica de cálculo de frete.
        """
        print(f"[LOG] Calculando frete para CEP: {cep} com peso {peso}kg")
        
        res = FreteResponse()

        res.valor = 20.0 + (peso * 2.0)
        res.prazo = "5 dias úteis"
        res.obs = "Entrega sujeita a condições climáticas."

        return res