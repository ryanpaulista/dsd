from spyne import ComplexModel, Unicode, Float

class FreteResponse(ComplexModel):
    """
        Define a estrutura da resposta.
        No WSD, isso será um 'complexType' com os seguintes elementos:
        - valor: Float
        - prazo: Unicode
        - obs: Unicode (opcional)
    """
    valor = Float
    peso = Float
    prazo = Unicode
    obs = Unicode