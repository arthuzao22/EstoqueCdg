# Generated by Django 2.2 on 2024-12-27 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formato', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formato',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
