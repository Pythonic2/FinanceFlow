# Generated by Django 4.2.7 on 2023-11-25 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_fluxodecaixa_data_final_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fluxodecaixa',
            name='necessidade',
            field=models.CharField(choices=[('essemcial', 'Essencial'), ('desejos', 'Desejos (Não essencial)'), ('investimetos', 'Investimentos')], default='essencial', max_length=12),
        ),
    ]
