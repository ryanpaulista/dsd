from ..models import Produto

class CompraService:
    @staticmethod
    def registrar_compra(id_produto: int, quantidade: int):
        produto = Produto.objects.get(id=id_produto)
        produto.estoque -= quantidade
        produto.save()

        return produto.estoque

