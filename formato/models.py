from django.db import models

class Formato(models.Model):
    formato = models.CharField(max_length=255)
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.formato
