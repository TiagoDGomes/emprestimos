
import json

from django import forms
from django.core.validators import BaseValidator
from django.db.models.query import Q
from django.forms.fields import MultipleChoiceField
from django.core.exceptions import ValidationError

from .models import ItemEmprestimo, Pessoa


class ReservaField(forms.CharField):
    pass
        

class ReservaForm(forms.Form):
    info = ReservaField(required=True)       
    def clean_info(self):
        info_d = json.loads(self.cleaned_data['info'])
        if not 'pessoa_responsavel' in info_d or not info_d['pessoa_responsavel']:
            raise ValidationError('Pessoa responsável ausente')
        if not 'lista_itens' in info_d or not info_d['lista_itens']:
            raise ValidationError('Lista vazia')
        try:
            self.cleaned_data['pessoa_responsavel'] = Pessoa.objects.get(id=info_d['pessoa_responsavel'])
        except:
            raise ValidationError('Pessoa inexistente')
        self.cleaned_data['itens'] = []
        for item_dict in info_d['lista_itens']:
            item = ItemEmprestimo.objects.get(id=item_dict['item'])
            data_hora_inicio = item_dict['data_hora_inicio']
            self.cleaned_data['itens'].append(dict(item=item,data_hora_inicio=data_hora_inicio))


    def fazer_reserva(self):
        for it in self.cleaned_data['itens']:
            item = it['item']
            data_hora_inicio = it['data_hora_inicio']
            item.fazer_reserva(self.cleaned_data['pessoa_responsavel'], data_hora_inicio)



class BuscaForm(forms.Form):
    texto = forms.CharField(required=False,)
    exc_p = forms.CharField(required=False,)
    exc_i = forms.CharField(required=False,)
    def fazer_busca(self):
        response = {}
        try:
            texto = self.cleaned_data['texto']
            if texto != '':                
                try:
                    excecao_pessoas = [ int(x) for x in self.cleaned_data['exc_p'].split(',') ]
                except:
                    excecao_pessoas = []
                pesquisa_pessoa = [{'nome': x.nome,
                                    'matricula': x.matricula,
                                    'detalhes': x.detalhes,
                                    'observacao': x.observacao,
                                    'bloqueio': x.bloqueio,
                                    'reservas': x.reservas_atuais}
                                   for x in Pessoa.objects.filter(Q(nome__contains=texto) |
                                                                  Q(matricula=texto) |
                                                                  Q(cpf=texto)
                                                                  ).exclude(id__in=excecao_pessoas)]
                
                try:
                    excecao_itens = [ int(x) for x in self.cleaned_data['exc_p'].split(',') ]
                except:
                    excecao_itens = []
                pesquisa_itens = [{'codigo': x.codigo,
                                   'nome': x.nome,
                                   'status': x.status}
                                  for x in ItemEmprestimo.objects.filter(Q(nome__contains=texto) |
                                                                         Q(palavras_chave__contains=texto) |
                                                                         Q(codigo__contains=texto)).exclude(id__in=excecao_itens)]
                response = dict(texto=texto,
                                pessoas=pesquisa_pessoa,
                                itens=pesquisa_itens)
        except KeyError:
            pass
        return response
