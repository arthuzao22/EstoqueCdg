# Generated by Django 3.2.25 on 2024-12-20 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_produto_estoquemin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto',
            old_name='estoquemin',
            new_name='estoquemin',
        ),
    ]
