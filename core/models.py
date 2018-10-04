from django.db import models
from localflavor.br.forms import BRCPFField


class Pessoa(models.Model):
    nome = models.CharField(max_length=125)
    cpf = BRCPFField()
    matricula = models.CharField(
        max_length=35, unique=True, null=True, blank=True)


class ItemEmprestimo(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Item para empréstimo'
        verbose_name_plural = 'Itens para empréstimo'


class Emprestimo(models.Model):
    item = models.ForeignKey(ItemEmprestimo, on_delete=models.CASCADE)
    pessoa_responsavel = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE, related_name='responsavel')
    pessoa_retirada = models.ForeignKey(
        Pessoa, null=True, blank=True, on_delete=models.CASCADE, related_name='pessoa_retirada')
    data_retirada_programada = models.DateTimeField(null=True)
    data_devolucao_programada = models.DateTimeField(null=True)
    data_retirada = models.DateTimeField(null=True)
    data_devolucao = models.DateTimeField(null=True)
