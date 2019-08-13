
import datetime
import json

from django.urls.base import reverse
from django.utils import timezone

from core.models import (STATUS_ITEM, Emprestimo, ItemEmprestimo, Pessoa,
                         TipoItem)

from .base import TestCaseBase


class TestBuscaPadrao(TestCaseBase):

    def test_vazio(self):
        response = self.client.get(reverse('resultado_busca'))
        self.assertContains(response, '{}')
        
    def test_vazio_2(self):
        response = self.busca()
        self.assertEqual(response, {})

    def test_busca_pessoa_nome_part(self):
        response = self.busca(self.trecho_nome_pessoa)
        self.assertEqual(response['pessoas'][0]['nome'], self.pessoa.nome)
        self.assertEqual(len(response['itens']), 0)

    def test_busca_pessoa_nao_bloqueada(self):
        response = self.busca_pessoa()
        self.assertIsNone(response['pessoas'][0]['bloqueio'])

    def test_busca_itens_emprestados_pessoa(self):
        reservas = self.sala.pedir_agora(self.pessoa, self.amanha_hora_1)
        response = self.busca_pessoa()
        self.assertEqual(response['pessoas'][0]['reservas'][0]['item'], self.sala.nome)
        self.assertEqual(response['pessoas'][0]['reservas'][0]['id'], reservas[0].id)
        self.assertEqual(response['pessoas'][0]['reservas'][0]['item_id'], self.sala.id)
        self.assertEqual(response['pessoas'][0]['reservas'][0]['data_hora_fim'], reservas[0].data_hora_fim.isoformat())


    def test_busca_pessoa_bloqueada(self):
        self.pessoa.bloquear_emprestimos_ate = self.amanha_hora_1
        self.pessoa.save()
        response = self.busca_pessoa()
        self.assertIsNotNone(response['pessoas'][0]['bloqueio'])

    def test_busca_pessoa_desbloqueada(self):
        self.pessoa.bloquear_emprestimos_ate = self.ontem_hora_1
        self.pessoa.save()
        response = self.busca_pessoa()
        self.assertIsNone(response['pessoas'][0]['bloqueio'])

    def test_busca_pessoa_matricula(self):
        response = self.busca(self.pessoa.matricula)
        self.assertEqual(response['pessoas'][0]['nome'], self.pessoa.nome)

    def test_busca_pessoa_cpf(self):
        response = self.busca(self.pessoa.cpf)
        self.assertEqual(response['pessoas'][0]['nome'], self.pessoa.nome)

    def test_busca_pessoa_cpf_part(self):
        response = self.busca(self.pessoa.cpf[1:3])
        self.assertEqual(len(response['pessoas']), 0)

    def test_busca_pessoa_matricula_part(self):
        response = self.busca(self.pessoa.matricula[1:3])
        self.assertEqual(len(response['pessoas']), 0)
    
    def test_item_nome(self):
        response = self.busca(self.sala.nome)
        self.assertEqual(response['itens'][0]['nome'], self.sala.nome)
        self.assertEqual(len(response['pessoas']), 0)

    def test_item_codigo(self):
        response = self.busca(self.sala.codigo)
        self.assertEqual(response['itens'][0]['nome'], self.sala.nome)
        self.assertEqual(len(response['itens']), 1)

    def test_item_palavra_chave(self):
        response = self.busca(self.sala.palavras_chave.split(' ')[0])
        self.assertEqual(response['itens'][0]['nome'], self.sala.nome)


class TestBuscaItemUnitario(TestCaseBase):
    
    def test_reserva_futura(self):
        self.sala.fazer_reserva(self.pessoa, self.amanha_hora_1, self.amanha_hora_2,)
        response = self.busca_sala()  
        self.assertEqual(response['itens'][0]['status']['code'], STATUS_ITEM['disponivel']['code'])

    def test_reservado_necessita_confirmar_retirada_e_nao_retirou(self):
        self.sala.fazer_reserva(self.pessoa, self.hoje_hora_1, self.hoje_hora_2,)
        response = self.busca_sala()  
        self.assertEqual(response['itens'][0]['status']['code'], STATUS_ITEM['ret_atrasada']['code'])

    def test_reservado_bloqueio_alerta(self):
        self.sala.bloqueio_minutos_antes = 60
        self.sala.save()
        self.sala.fazer_reserva(self.pessoa, self.hoje_hora_2, self.hoje_hora_3,)
        response = self.busca_sala()  
        self.assertEqual(response['itens'][0]['status']['code'], STATUS_ITEM['reservado']['code'])

    def test_reservado_e_nao_necessita_confirmar_retirada(self):
        self.sala.necessita_confirmacao_retirada = False
        self.sala.save()
        self.sala.fazer_reserva(self.pessoa, self.hoje_hora_1, self.hoje_hora_2,)
        response = self.busca_sala()  
        self.assertEqual(response['itens'][0]['status']['code'], STATUS_ITEM['utilizado']['code'])
    
    def test_reservado_precisa_devolver_e_nao_devolveu(self):
        self.sala.fazer_reserva(self.pessoa, self.ontem_hora_1, self.ontem_hora_2,)
        response = self.busca_sala()  
        self.assertEqual(response['itens'][0]['status']['code'], STATUS_ITEM['devol_atrasada']['code'])
    
    def test_reservado_precisa_devolver_e_devolveu(self):
        reservas = self.sala.fazer_reserva(self.pessoa, self.ontem_hora_1, self.ontem_hora_2,)
        reservas[0].fazer_devolucao()
        response = self.busca_sala()  
        self.assertEqual(response['itens'][0]['status']['code'], STATUS_ITEM['disponivel']['code'])
    
    def test_reservado_nao_precisa_devolver(self):
        self.sala.necessita_confirmacao_devolucao = False
        self.sala.save()
        self.sala.fazer_reserva(self.pessoa, self.ontem_hora_1, self.ontem_hora_2,)
        response = self.busca_sala()  
        self.assertEqual(response['itens'][0]['status']['code'], STATUS_ITEM['disponivel']['code'])
        
    def test_fila(self):
        self.sala.reserva_por_fila = True
        self.sala.save()
        self.sala.fazer_reserva(self.pessoa,)
        response = self.busca_sala()  
        self.assertEqual(response['itens'][0]['status']['code'], STATUS_ITEM['fila']['code'])
    
    def test_ja_escolhido(self):
        response = self.busca(self.sala.codigo, self.sala.id)
        print (response)
        self.assertEqual(len(response['itens']), 0)

class TesteBuscaItemMulti(TestCaseBase):
       
    def test_item(self):
        response = self.busca("LAP")
        self.assertEqual(response['itens'][0]['nome'], self.lapis.nome)
        self.assertEqual(response['itens'][0]['status']['utilizado'], 0)
        self.assertEqual(response['itens'][0]['status']['restante'], 3)
        self.assertEqual(response['itens'][0]['status']['code'], 10)

    def test_item_pedir_agora(self):
        self.lapis.pedir_agora(self.pessoa)
        response = self.busca_lapis()      
        self.assertEqual(response['itens'][0]['status']['utilizado'], 1)
        self.assertEqual(response['itens'][0]['status']['restante'], 2)
        self.assertEqual(response['itens'][0]['status']['attr_class'], 'success')
      
        self.lapis.pedir_agora(self.pessoa)
        response = self.busca_lapis()
        self.assertEqual(response['itens'][0]['status']['utilizado'], 2)
        self.assertEqual(response['itens'][0]['status']['restante'], 1)
        self.assertEqual(response['itens'][0]['status']['attr_class'], 'success')

        self.lapis.pedir_agora(self.pessoa)
        response = self.busca_lapis()
        self.assertEqual(response['itens'][0]['status']['utilizado'], 3)
        self.assertEqual(response['itens'][0]['status']['restante'], 0)
        self.assertEqual(response['itens'][0]['status']['attr_class'], 'warning')

    def test_item_pedir_varios_agora(self):
        emprestimos = self.lapis.pedir_agora(self.pessoa, quantidade=3)
        self.assertEqual(len(emprestimos), 3)        
        response = self.busca_lapis()      
        self.assertEqual(response['itens'][0]['status']['utilizado'], 3)
        self.assertEqual(response['itens'][0]['status']['restante'], 0)
        self.assertEqual(response['itens'][0]['status']['attr_class'], 'warning')

        
    def test_item_devolvido(self):
        emprestimos = self.lapis.pedir_agora(self.pessoa)
        emprestimos[0].fazer_devolucao()
        response = self.busca_lapis()      
        self.assertEqual(response['itens'][0]['status']['utilizado'], 0)
        self.assertEqual(response['itens'][0]['status']['restante'], 3)
        
        
    def test_item_varios_devolvidos(self):
        emprestimos = self.lapis.pedir_agora(self.pessoa, quantidade=3)
        emprestimos[0].fazer_devolucao()
        emprestimos[1].fazer_devolucao()
        response = self.busca_lapis()      
        self.assertEqual(response['itens'][0]['status']['utilizado'], 1)
        self.assertEqual(response['itens'][0]['status']['restante'], 2)
