# Generated by Django 2.2.4 on 2019-08-10 19:00

from django.db import migrations, models
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_itememprestimo_reserva_por_fila'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='cpf',
            field=models.CharField(max_length=14, null=True, validators=[localflavor.br.models.BRCPFField]),
        ),
    ]
