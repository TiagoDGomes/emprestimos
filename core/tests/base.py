import datetime
import json

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from core.models import (STATUS_ITEM, Emprestimo, ItemEmprestimo, Pessoa,
                         TipoItem)


class TestCaseBase(TestCase):
    def setUp(self):
        self.pessoa = Pessoa.objects.create(
            nome="FULANO DE TAL", matricula="A98765")
        self.trecho_nome_pessoa = "FUL"
        self.pessoa.cpf = '12345678909'
        self.trecho_cpf = '12345'
        self.pessoa.save()
        tipo_item = TipoItem.objects.create()
        tipo_item.nome = 'SALA'
        tipo_item.save()
        self.sala = ItemEmprestimo.objects.create()
        self.sala.tipo = tipo_item
        self.sala.nome = 'SALA DE AULA 1 - BLOCO A'
        self.trecho_item_nome = 'SALA'
        self.sala.codigo = 'SA1'
        self.sala.palavras_chave = 'SL1A BLA1S'
        self.trecho_palavra_chave = 'SL1A'
        self.sala.save()
        self.amanha_hora_1 = timezone.now() + datetime.timedelta(days=1)
        self.amanha_hora_2 = timezone.now() + datetime.timedelta(days=1, hours=1)
        self.hoje_hora_1 = timezone.now() - datetime.timedelta(hours=1)
        self.hoje_hora_2 = timezone.now() + datetime.timedelta(hours=1)
        self.hoje_hora_3 = timezone.now() + datetime.timedelta(hours=2)
        self.ontem_hora_1 = timezone.now() - datetime.timedelta(days=1, hours=1)
        self.ontem_hora_2 = timezone.now() - datetime.timedelta(days=1)
        tipo_item = TipoItem.objects.create()
        tipo_item.nome = 'MATERIAL ESCOLAR'
        tipo_item.save()
        self.lapis = ItemEmprestimo.objects.create()
        self.lapis.tipo = tipo_item
        self.lapis.nome = 'LAPIS'
        self.lapis.codigo = 'LP'
        self.lapis.quantidade_total = 3
        self.lapis.palavras_chave = 'SL1A BLA1S'
        self.lapis.save()  

    def busca(self, texto='', exc_p='', exc_i=''):
        response = json.loads(self.client.get(reverse('resultado_busca'), dict(texto=texto, exc_p=exc_p, exc_i=exc_i)).content)
        return (response)    

    def busca_pessoa(self):
        return self.busca(self.pessoa.nome)

    def busca_sala(self):
        return self.busca('SALA')

    def busca_lapis(self):
        return self.busca('LAP')

