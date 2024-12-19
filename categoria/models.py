from django.db import models

class Categoria(models.Model):
    categoria = models.CharField(max_length=255)
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.categoria
