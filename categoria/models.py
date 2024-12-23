from django.db import models

class Categoria(models.Model):
    categoria = models.CharField(max_length=255)
    img = models.ImageField(upload_to='images/', null=True, blank=True)  # Novo campo de imagem
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.categoria
