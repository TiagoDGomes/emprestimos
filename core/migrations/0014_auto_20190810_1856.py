# Generated by Django 2.2.4 on 2019-08-10 21:56

from django.db import migrations, models
import localflavor.br.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_pessoa_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='itememprestimo',
            name='bloqueio_minutos_antes',
            field=models.IntegerField(default=60, help_text='Impede de reservar minutos antes da próxima reserva', null=True),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='data_hora_inicio',
            field=models.DateTimeField(null=True, verbose_name='Data/hora de início'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='bloquear_emprestimos_ate',
            field=models.DateField(blank=True, null=True, verbose_name='bloquear empréstimos até'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[localflavor.br.validators.BRCPFValidator()], verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='observacao',
            field=models.TextField(blank=True, null=True, verbose_name='observação'),
        ),
    ]
