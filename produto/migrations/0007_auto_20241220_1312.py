# Generated by Django 3.2.25 on 2024-12-20 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_auto_20241220_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='id_formato',
        ),
        migrations.AlterField(
            model_name='produto',
            name='formato',
            field=models.CharField(blank=True, choices=[('640x880', '640x880'), ('660x960', '660x960')], max_length=255, null=True),
        ),
    ]
