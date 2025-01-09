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
    status = models.IntegerField()
    id_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)  # Alterado para PROTECT
    id_formato = models.ForeignKey(Formato, on_delete=models.PROTECT)  # Alterado para PROTECT
    unidades = models.IntegerField()
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    id_produto = models.ForeignKey(
        'Produto', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="estoques"
    )
    qtde = models.IntegerField()
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_produto.nome if self.id_produto else 'Produto Indefinido'} - {self.qtde} unidades"
    
    def save(self, *args, **kwargs):
        if self.qtde < 0:
            raise ValueError("A qtde não pode ser negativa.")
        super().save(*args, **kwargs)
