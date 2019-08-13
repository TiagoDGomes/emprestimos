import datetime
import json
from datetime import timedelta
from os.path import normcase

from django.db import models
from django.db.models import Q
from django.db.models.fields import IntegerField
from django.utils import timezone
from localflavor.br.validators import BRCPFValidator
from django.core.exceptions import ValidationError

STATUS_ITEM = dict(    
    
    problema_registro=dict(
        code=-7,
        verbose='problema no registro',
        attr_class='danger'
    ),
    multiplo_ocupado=dict(
        code=-6,
        verbose='todos em uso',
        attr_class='warning'
    ),
    quebrado=dict(
        code=-5,
        verbose='quebrado',
        attr_class='danger'
    ),
    perdido=dict(
        code=-4,
        verbose='perdido',
        attr_class='danger'
    ),
    devol_atrasada=dict(
        code=-3,
        verbose='devolução atrasada',
        attr_class='danger'
    ),
    ret_atrasada=dict(
        code=-2,
        verbose='retirada atrasada',
        attr_class='danger'
    ),
    bloqueado=dict(
        code=-1,
        verbose='bloqueado',
        attr_class='default'
    ),
    desconhecido=dict(
        code=0,
        verbose='desconhecido',
        attr_class='default'
    ),
    disponivel=dict(
        code=1,
        verbose='disponível',
        attr_class='success'
    ),
    multiplo=dict(
        code=10,
        verbose='disponibilidade por volume',
        attr_class='success'
    ),
    reservado=dict(
        code=11,
        verbose='reservado',
        attr_class='danger'
    ),
    utilizado=dict(
        code=12,
        verbose='em utilização',
        attr_class='warning'
    ),
    fila=dict(
        code=13,
        verbose='em fila de espera',
        attr_class='warning',
    )
)


class Pessoa(models.Model):
    nome = models.CharField(max_length=125)
    cpf = models.CharField(max_length=14, null=True, blank=True, validators=[BRCPFValidator(),], verbose_name='CPF')
    matricula = models.CharField(
        max_length=35, unique=True, null=True, blank=True)
    detalhes = models.TextField(null=True, blank=True,)
    observacao = models.TextField(null=True, blank=True, verbose_name='observação')
    bloquear_emprestimos_ate = models.DateField(null=True, blank=True, verbose_name='bloquear empréstimos até',)

    def __str__(self):
        return self.nome

    @property
    def bloqueio(self):
        if self.bloquear_emprestimos_ate:
            now = timezone.now()
            if self.bloquear_emprestimos_ate >= now.date():
                return self.bloquear_emprestimos_ate.isoformat()
        return None

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Pessoa, self).save(*args, **kwargs)

    @property
    def reservas_atuais(self):
        reservas = self.emprestimos.filter(Q(data_devolucao__lt=timezone.now())|
                            (Q(data_hora_fim__gt=timezone.now())&Q(item__necessita_confirmacao_devolucao=True)))
        
        return [{'item': x.item.nome, 'item_id': x.item.id, 'id': x.id, 'data_hora_fim': x.data_hora_fim.isoformat()} for x in reservas]

class TipoItem(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True,)

    class Meta:
        verbose_name = 'tipo de item para empréstimo'
        verbose_name_plural = 'tipos de item para empréstimo'

    def __str__(self):
        return self.nome


class ItemEmprestimo(models.Model):
    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=50, unique=True, null=True, )
    observacoes = models.TextField(null=True, blank=True)
    tipo = models.ForeignKey(
        TipoItem, null=True, blank=True, on_delete=models.CASCADE)
    minutos_utilizacao_limite = models.IntegerField(
        null=True, blank=True, help_text="Defina o tempo máximo permitido para utilização")
    quantidade_total = models.IntegerField(
        null=True, blank=True, default=1, help_text="Utilize um valor diferente de 1 para itens que não necessita de controle individual (ex.: bens não patrimoniados). ")
    palavras_chave = models.TextField(
        null=True, blank=True, help_text="Várias palavras separadas por espaços que auxiliam na busca")
    necessita_confirmacao_retirada = models.BooleanField(
        null=True, default=True, )
    necessita_confirmacao_devolucao = models.BooleanField(
        null=True, default=True, )
    reserva_bloqueada = models.BooleanField(
        null=True, default=False, help_text="Impede que este item seja reservado")
    reserva_por_fila = models.BooleanField(
        null=True, default=False, help_text='Permite apenas reserva por fila de espera'
    )
    bloqueio_minutos_antes = models.IntegerField(null=True, blank=True, default=60, help_text='Impede de reservar minutos antes da próxima reserva (não tem efeito para item com quantidade total maior que 1)')
    
    class Meta:
        verbose_name = 'item para empréstimo'
        verbose_name_plural = 'itens para empréstimo'


    def __str__(self):
        return self.nome


    def fazer_reserva(self, pessoa_responsavel, data_hora_inicio=None, data_hora_fim=None, observacoes='', quantidade=1):
        reservas = []
        if pessoa_responsavel.bloqueio:
            raise ValidationError('Pessoa bloqueada')
        print(('fazer reserva', self.quantidade_total, self.status['code']))
        if self.quantidade_total == 1 and (self.status['code'] < 1 or self.status['code'] > 10):
            print(('fazer reserva', self.status))
            raise ValidationError("Não é possível reservar. Status: {}".format(self.status['verbose']))
        for _ in range(quantidade):
            emprestimo = Emprestimo.objects.create(item=self, pessoa_responsavel=pessoa_responsavel)
            emprestimo.data_hora_inicio = data_hora_inicio
            if data_hora_fim is not None:
                emprestimo.data_hora_fim = data_hora_fim
            emprestimo.save()
            reservas.append(emprestimo)
        return reservas


    def pedir_agora(self, pessoa_responsavel, data_hora_fim=None, observacoes='', quantidade=1):
        return self.fazer_reserva(pessoa_responsavel, timezone.now(), data_hora_fim, observacoes, quantidade)

    

    

    @property
    def status(self):
        if self.reserva_bloqueada:
            return STATUS_ITEM['bloqueado']
        
        now = timezone.now()
        status_utilizacao = {}
        if self.quantidade_total > 1:
            status_utilizacao['utilizado'] = len(self.reserva_atual)
            status_utilizacao['restante'] = self.quantidade_total - len(self.reserva_atual)
            key = 'multiplo' if status_utilizacao['restante'] > 0 else 'multiplo_ocupado'           
            
        elif not self.reserva_atual:
            key = 'disponivel'
        else:            
            res_atual = self.reserva_atual[0]
            key = 'desconhecido'
            status_utilizacao = dict(
                utilizador_nome=res_atual.pessoa_responsavel.nome,
                utilizador_matricula=res_atual.pessoa_responsavel.matricula,
            )
            if self.reserva_por_fila:
                key = 'fila'
            else:
                if res_atual.data_hora_inicio is None or res_atual.data_hora_fim is None:
                    key = 'problema_registro'
                    status_utilizacao['data_hora_valida'] = False
                else:
                    status_utilizacao['data_hora_valida'] = True
                    status_utilizacao['data_hora_inicio'] = res_atual.data_hora_inicio.isoformat()
                    status_utilizacao['data_hora_fim'] = res_atual.data_hora_fim.isoformat()
                    if res_atual.data_hora_inicio > now:  # se nao iniciou
                        key = 'disponivel'
                        hora_bloqueio = res_atual.data_hora_inicio - timedelta(minutes=self.bloqueio_minutos_antes)                        
                        if hora_bloqueio <= now:
                            key = 'reservado'
                    else:
                        key = 'utilizado'
                        if res_atual.data_hora_fim < now:  # se acabou
                            key = 'disponivel'
                            if self.necessita_confirmacao_devolucao:
                                if res_atual.data_devolucao is None:
                                    key = 'devol_atrasada'
                        elif self.necessita_confirmacao_retirada:
                            if res_atual.data_retirada is None:
                                key = 'ret_atrasada'
                                    
        z = status_utilizacao.copy()
        z.update(STATUS_ITEM[key])
        return z

    @property
    def historico(self):
        return None

    @property
    def reserva_atual(self):
        lasts = Emprestimo.objects.filter(item=self).filter(
            Q(data_devolucao__isnull=True) & Q(item__necessita_confirmacao_devolucao=True)
        )
        return lasts
        


class Emprestimo(models.Model):
    item = models.ForeignKey(ItemEmprestimo, on_delete=models.CASCADE)
    pessoa_responsavel = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE, related_name='emprestimos', verbose_name='Pessoa responsável')
    pessoa_retirada = models.ForeignKey(
        Pessoa, null=True, blank=True, on_delete=models.CASCADE, related_name='pessoa_retirada', verbose_name='Pessoa a retirar')
    data_hora_inicio = models.DateTimeField(
        null=True, blank=True, verbose_name='Data/hora de início',)
    data_hora_fim = models.DateTimeField(
        null=True, blank=True, verbose_name='Data/hora de término',)
    data_retirada = models.DateTimeField(
        null=True, blank=True, verbose_name='Data/hora da retirada')
    data_devolucao = models.DateTimeField(
        null=True, blank=True, verbose_name='Data/hora de devolução')

    class Meta:
        verbose_name = 'empréstimo registrado'
        verbose_name_plural = 'empréstimos registrados'

    def __str__(self):
        return "{item} por {nome} em {data}".format(item=self.item.nome, nome=self.pessoa_responsavel.nome, data=self.data_hora_inicio)

    def fazer_retirada(self, pessoa_retirada, data_retirada=datetime.datetime.now, observacoes=''):
        pass

    def fazer_devolucao(self, data_devolucao=None, observacoes=''):
        if not data_devolucao:
            data_devolucao = timezone.now()
        self.data_devolucao = data_devolucao
        self.save()

    def __init__(self, *args, **kwargs):
        super(Emprestimo, self).__init__(*args, **kwargs)
        self._meta.get_field('data_hora_inicio').validators = [self._validator_data_hora_inicio]
        self._meta.get_field('data_hora_fim').validators = [self._validator_data_hora_fim]
        self._meta.get_field('data_devolucao').validators = [self._validator_data_devolucao]

    def _validator_data_hora_inicio(self, value):
        if self.data_hora_inicio and self.item.reserva_por_fila:
            raise ValidationError('Este item permite apenas reservas por fila de espera')
        
    def _validator_data_hora_fim(self, value):
        if self.data_hora_fim and self.data_hora_fim < self.data_hora_inicio:
            raise ValidationError('Não é possivel definir uma data anterior à reserva')

    def _validator_data_devolucao(self, value):         
        if self.data_devolucao and self.data_devolucao < self.data_hora_inicio:
            raise ValidationError('Não é possivel definir uma data anterior à reserva')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Emprestimo, self).save(*args, **kwargs)