
import json

from django.test import TestCase
from django.urls.base import reverse
import datetime
from django.utils import timezone


from core.models import ItemEmprestimo, Pessoa, TipoItem, Emprestimo, STATUS_ITEM

def TestErros(TestCase):
    self.pessoa = Pessoa.objects.create(
        nome="FULANO DE TAL", matricula="A98765")
    self.pessoa.cpf = '12345678909'
    self.pessoa.save()
    tipo_item = TipoItem.objects.create()
    tipo_item.nome = 'SALA'
    tipo_item.save()
    self.item = ItemEmprestimo.objects.create()
    self.item.tipo = tipo_item
    self.item.nome = 'SALA DE AULA 1 - BLOCO A'
    self.item.codigo = 'A1'
    self.item.palavras_chave = 'SL1A BLA1S'
    self.item.save()
