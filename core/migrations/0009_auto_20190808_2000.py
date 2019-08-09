# Generated by Django 2.2.4 on 2019-08-08 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190808_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipoitem',
            name='minutos_utilizacao_padrao',
        ),
        migrations.AddField(
            model_name='pessoa',
            name='bloquear_emprestimos_ate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='detalhes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='observacao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='itememprestimo',
            name='quantidade_total',
            field=models.IntegerField(blank=True, default=1, help_text='Utilize um valor diferente de 1 para itens que não necessita de controle individual (ex.: bens não patrimoniados). ', null=True),
        ),
    ]
