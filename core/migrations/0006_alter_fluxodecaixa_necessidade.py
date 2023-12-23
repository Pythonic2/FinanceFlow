# Generated by Django 4.2.7 on 2023-12-22 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_fluxodecaixa_necessidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fluxodecaixa',
            name='necessidade',
            field=models.CharField(choices=[('essencial', 'Essencial'), ('desejos', 'Desejo (Não essencial)'), ('investimetos', 'Investimento'), ('nao se aplica', 'Não se aplica')], default='essencial', max_length=13),
        ),
    ]