# Generated by Django 4.2.7 on 2023-11-25 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_fluxodecaixa_data_final_fluxodecaixa_periodicidade_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fluxodecaixa',
            name='data_final',
        ),
        migrations.RemoveField(
            model_name='fluxodecaixa',
            name='periodicidade',
        ),
        migrations.RemoveField(
            model_name='fluxodecaixa',
            name='recorrente',
        ),
        migrations.AlterField(
            model_name='fluxodecaixa',
            name='tipo',
            field=models.CharField(choices=[('renda', 'Renda'), ('despesa', 'Despesa')], max_length=8),
        ),
    ]