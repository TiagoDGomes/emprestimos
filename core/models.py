import datetime
from os.path import normcase

from django.db import models
from django.db.models import Q
from django.utils import timezone
from localflavor.br.validators import BRCPFValidator

STATUS_ITEM = dict(
    quebrado=dict(
        code=-4,
        verbose='quebrado',
        attr_class='danger'
    ),
    perdido=dict(
        code=-3,
        verbose='perdido',
        attr_class='danger'
    ),
    devol_atrasada=dict(
        code=-2,
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

    class Meta:
        verbose_name = 'item para empréstimo'
        verbose_name_plural = 'itens para empréstimo'

    def __str__(self):
        return self.nome

    def reservar(self, pessoa_responsavel, data_retirada_programada, data_devolucao_programada=None, observacoes='', retirada_na_hora=False):
        pass

    @property
    def status(self):
        if self.reserva_bloqueada:
            return STATUS_ITEM['bloqueado']
        
        now = timezone.now()
        status_utilizacao = {}
        if self.quantidade_total > 1:
            key = 'multiplo'
            status_utilizacao['utilizado'] = len(self.reserva_atual)
            status_utilizacao['restante'] = self.quantidade_total - len(self.reserva_atual)
            
        elif not self.reserva_atual:
            key = 'disponivel'
        else:
            print(self.reserva_atual)
            res_atual = self.reserva_atual[0]
            key = 'desconhecido'
            print(res_atual.data_hora_inicio)
            status_utilizacao = dict(
                utilizador_nome=res_atual.pessoa_responsavel.nome,
                utilizador_matricula=res_atual.pessoa_responsavel.matricula,
            )
            if self.reserva_por_fila:
                key = 'fila'
            else:
                if res_atual.data_hora_inicio is None or res_atual.data_hora_fim is None:
                    status_utilizacao['data_hora_valida'] = False
                else:
                    status_utilizacao['data_hora_valida'] = True
                    status_utilizacao['data_hora_inicio'] = res_atual.data_hora_inicio.isoformat()
                    status_utilizacao['data_hora_fim'] = res_atual.data_hora_fim.isoformat()
                    if res_atual.data_hora_inicio > now:  # se nao iniciou
                        key = 'disponivel'
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
        last = Emprestimo.objects.filter(item=self).filter(
            Q(data_devolucao__isnull=True) & Q(item__necessita_confirmacao_devolucao=True)
        )
        return last
        


class Emprestimo(models.Model):
    item = models.ForeignKey(ItemEmprestimo, on_delete=models.CASCADE)
    pessoa_responsavel = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE, related_name='responsavel', verbose_name='Pessoa responsável')
    pessoa_retirada = models.ForeignKey(
        Pessoa, null=True, blank=True, on_delete=models.CASCADE, related_name='pessoa_retirada', verbose_name='Pessoa a retirar')
    data_hora_inicio = models.DateTimeField(
        null=True, blank=True, verbose_name='Data/hora de início')
    data_hora_fim = models.DateTimeField(
        null=True, blank=True, verbose_name='Data/hora de término')
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

    def fazer_devolucao(self, data_devolucao=datetime.datetime.now, observacoes=''):
        pass
