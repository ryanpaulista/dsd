from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    imagem_url = models.URLField(blank=True)

    def __str__(self):
        return self.nome