from django.db import models
from empresa.models import Empresa
from produto.models import Produto
from django.contrib.auth.models import User

class Movimentacoes(models.Model):
    TIPO_MOVIMENTACAO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Saída', 'Saída'),
    ]
    tipo_movimentacao = models.CharField(max_length=10, choices=TIPO_MOVIMENTACAO_CHOICES)
    qtde = models.IntegerField()
    data_chegada_saida = models.DateField()  # Certifique-se de que este campo está presente
    data = models.DateField(auto_now_add=True)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT) 
    id_usuario = models.ForeignKey(User, on_delete=models.PROTECT)    
    id_produto = models.ForeignKey(Produto, on_delete=models.PROTECT) 
