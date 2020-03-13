

from django.core.exceptions import ValidationError

from ..models import STATUS_ITEM

from .base import TestCaseBase


class TestErros(TestCaseBase):
    def test_reserva_pessoa_bloqueada(self):
        self.pessoa.bloquear_emprestimos_ate = self.amanha_hora_1.date()
        self.pessoa.save()
        with self.assertRaises(ValidationError):
            self.sala.pedir_agora(self.pessoa)

    def test_devolucao_ontem(self):
        reservas = self.sala.pedir_agora(self.pessoa)
        with self.assertRaises(ValidationError):
            reservas[0].fazer_devolucao(self.ontem_hora_1)

    def test_reservar_devolucao_ontem(self):
        with self.assertRaises(ValidationError):
            self.sala.fazer_reserva(self.pessoa, self.amanha_hora_2, self.amanha_hora_1)        
        
    def test_cpf_invalido(self):
        self.pessoa.cpf = '12345678900'
        with self.assertRaises(ValidationError):
            self.pessoa.save()

    def test_reservar_item_fila(self):
        self.sala.reserva_por_fila = True
        with self.assertRaises(ValidationError):
            self.sala.fazer_reserva(self.pessoa, self.amanha_hora_1,)
    
    def test_reservar_item_todos_ocupados(self):
        for i in range(self.lapis.quantidade_total):
            self.lapis.pedir_agora(self.pessoa,) 
        
        with self.assertRaises(ValidationError):
            self.lapis.pedir_agora(self.pessoa,) 
               
    def test_fazer_reserva_reservado(self): 
        self.sala.necessita_confirmacao_retirada = False
        self.sala.necessita_confirmacao_devolucao = True
        self.sala.save()    
        self.sala.pedir_agora(self.pessoa, self.amanha_hora_1,)
        print(self.sala.status)        
        with self.assertRaises(ValidationError):
            self.sala.pedir_agora(self.pessoa, self.amanha_hora_1,)
