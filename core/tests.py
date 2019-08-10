
import json

from django.test import TestCase
from django.urls.base import reverse
import datetime


from core.models import ItemEmprestimo, Pessoa, TipoItem


class TestBusca(TestCase):
    def setUp(self):
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

    def busca(self, texto=''):
        response = json.loads(self.client.get(reverse('resultado_busca'), dict(texto=texto)).content)
        #print(response)
        return (response)

    def test_vazio(self):
        response = self.client.get(reverse('resultado_busca'))
        self.assertContains(response, '{}')
        
    def test_vazio_2(self):
        response = self.busca()
        self.assertEqual(response, {})

    def test_busca_pessoa_nome(self):
        response = self.busca("FUL")
        self.assertEqual(response['pessoas'][0]['nome'], self.pessoa.nome)
        self.assertEqual(len(response['itens']), 0)

    def test_busca_pessoa_nao_bloqueada(self):
        response = self.busca("FULANO")
        self.assertIsNone(response['pessoas'][0]['bloqueio'])

    def test_busca_pessoa_bloqueada(self):
        self.pessoa.bloquear_emprestimos_ate = datetime.datetime.now()
        self.pessoa.save()
        response = self.busca("FULANO")
        self.assertIsNotNone(response['pessoas'][0]['bloqueio'])

    def test_busca_pessoa_desbloqueada(self):
        self.pessoa.bloquear_emprestimos_ate = datetime.datetime.now() - datetime.timedelta(days=1)
        self.pessoa.save()
        response = self.busca("FULANO")
        self.assertIsNone(response['pessoas'][0]['bloqueio'])

    def test_busca_pessoa_matricula(self):
        response = self.busca("A98765")
        self.assertEqual(response['pessoas'][0]['nome'], self.pessoa.nome)

    def test_busca_pessoa_cpf(self):
        response = self.busca("12345678909")
        self.assertEqual(response['pessoas'][0]['nome'], self.pessoa.nome)

    def test_busca_pessoa_cpf_part(self):
        response = self.busca("12345678")
        self.assertEqual(len(response['pessoas']), 0)

    def test_busca_pessoa_matricula_part(self):
        response = self.busca("987")
        self.assertEqual(len(response['pessoas']), 0)
    
    def test_item_nome(self):
        response = self.busca("SALA DE AULA")
        self.assertEqual(response['itens'][0]['nome'], self.item.nome)
        self.assertEqual(len(response['pessoas']), 0)

    def test_item_codigo(self):
        response = self.busca("A1")
        self.assertEqual(response['itens'][0]['nome'], self.item.nome)

    def test_item_palavra_chave(self):
        response = self.busca("SL1A")
        self.assertEqual(response['itens'][0]['nome'], self.item.nome)
