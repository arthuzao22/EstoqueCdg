from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.TextField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome
