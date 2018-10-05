from django.db import models
from localflavor.br.forms import BRCPFField
import datetime

class Pessoa(models.Model):
    nome = models.CharField(max_length=125)
    cpf = BRCPFField()
    matricula = models.CharField(max_length=35, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome


class TipoItem(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True,)
    horas_utilizacao_padrao = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = 'tipo de item para empréstimo'
        verbose_name_plural = 'tipos de item para empréstimo'

    def __str__(self):
        return self.nome 


STATUS = {
    'desconhecido': (0, 'desconhecido', 'default' ),
    'emprestado': (-1, 'emprestado', 'warning'),
    'atrasado': (-2, 'atrasado', 'danger'),
    'perdido': (-3, 'perdido', 'danger'),
    'quebrado': (-4, 'quebrado', 'danger'),
    'livre': (1, 'livre', 'success')
}
    

class ItemEmprestimo(models.Model):
    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=50, unique=True, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    tipo = models.ForeignKey(TipoItem, null=True, blank=True, on_delete=models.CASCADE)
    horas_utilizacao_limite = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'item para empréstimo'
        verbose_name_plural = 'itens para empréstimo'

    def __str__(self):
        return self.nome
    
    def reservar(self, pessoa_responsavel, data_retirada_programada, data_devolucao_programada=None, observacoes='', retirada_na_hora=False):
        pass
    
    @property
    def status(self):
        return STATUS['livre']

    @property
    def historico(self):
        return None


class Emprestimo(models.Model):
    item = models.ForeignKey(ItemEmprestimo, on_delete=models.CASCADE)
    pessoa_responsavel = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='responsavel')
    pessoa_retirada = models.ForeignKey(Pessoa, null=True, blank=True, on_delete=models.CASCADE, related_name='pessoa_retirada')
    data_retirada_programada = models.DateTimeField(null=True, blank=True)
    data_devolucao_programada = models.DateTimeField(null=True, blank=True)
    data_retirada = models.DateTimeField(null=True, blank=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)    
    
    class Meta:
        verbose_name = 'empréstimo registrado'
        verbose_name_plural = 'empréstimos registrados'

    def __str__(self):
        return "{item} por {nome} em {data}".format(item=self.item.nome, nome=self.pessoa_responsavel.nome, data=self.data_retirada_programada)

    
    def fazer_retirada(self, pessoa_retirada, data_retirada=datetime.datetime.now, observacoes=''):
        pass
    
    def fazer_devolucao(self, data_devolucao=datetime.datetime.now, observacoes=''):
        pass
    
