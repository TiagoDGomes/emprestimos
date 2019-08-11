

from .base import TestCaseBase
from django.urls.base import reverse
import json


class TestAcoes(TestCaseBase):
    def test_fazer_reserva(self):
        info = json.dumps(dict(
            pessoa_responsavel=self.pessoa.id,
            lista_itens=[
                dict(
                    item=self.sala.id,
                    data_hora_inicio=self.amanha_hora_1.isoformat()
                ),
                dict(
                    item=self.lapis.id,
                    data_hora_inicio=self.amanha_hora_1.isoformat()
                ),
                
            ]))

        self.client.post(reverse('fazer_reserva'), data={'info': info})
        self.assertEqual(len(self.sala.reserva_atual), 1)
        self.assertEqual(self.sala.reserva_atual[0].data_hora_inicio, self.amanha_hora_1)
        self.assertEqual(self.lapis.reserva_atual[0].data_hora_inicio, self.amanha_hora_1)
