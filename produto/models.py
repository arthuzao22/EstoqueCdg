from django.db import models
from categoria.models import Categoria
from formato.models import Formato

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    FORMATO = [
        ('640x880', '640x880'),
        ('660x960', '660x960')
    ]
    formato = models.CharField(max_length=255, choices=FORMATO, null=True, blank=True)  # Permite nulo
    estoquemin = models.IntegerField()
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    id_formato = models.ForeignKey(Formato, on_delete=models.CASCADE)  # Formato está aqui
    unidades = models.IntegerField()
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_produto.nome} - {self.qtde} unidades"


