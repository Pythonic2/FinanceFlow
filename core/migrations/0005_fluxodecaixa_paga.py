# Generated by Django 4.2.7 on 2023-11-15 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_categoria_orcamento_fluxodecaixa_categoria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fluxodecaixa',
            name='paga',
            field=models.BooleanField(default=False),
        ),
    ]