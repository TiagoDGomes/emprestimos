# Generated by Django 2.2.4 on 2019-08-08 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190808_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimo',
            name='data_devolucao_programada',
        ),
        migrations.RemoveField(
            model_name='emprestimo',
            name='data_retirada_programada',
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='data_hora_fim',
            field=models.DateTimeField(blank=True, help_text='Data/hora de término', null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='data_hora_inicio',
            field=models.DateTimeField(blank=True, help_text='Data/hora de início', null=True),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='data_devolucao',
            field=models.DateTimeField(blank=True, help_text='Data/hora de devolução', null=True),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='data_retirada',
            field=models.DateTimeField(blank=True, help_text='Data/hora da retirada', null=True),
        ),
    ]