# Generated by Django 2.2 on 2025-01-09 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0011_auto_20250109_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='status',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
