from django.db import models

# Create your models here.
class Kanban(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('todo', 'To Do'), ('in-progress', 'In Progress'), ('done', 'Done')], default='todo')
