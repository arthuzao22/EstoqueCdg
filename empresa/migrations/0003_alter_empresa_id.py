
"""Generated migration to alter Empresa.id to BigAutoField."""
from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		("empresa", "0002_auto_20241227_0903"),
	]

	operations = [
		migrations.AlterField(
			model_name="empresa",
			name="id",
			field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
		),
	]
