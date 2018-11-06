
from django import forms
from .models import Pessoa, ItemEmprestimo
from django.db.models.query import Q


class PesquisaEmprestimoForm(forms.Form):
    pessoa_pesquisada = forms.ModelChoiceField(queryset=Pessoa.objects,required=False,)
    texto_pesquisado = forms.CharField(required=False,)
    resultados = forms.ModelMultipleChoiceField(queryset=None)

    def clean_resultados(self):
        item_pesquisado_texto = self.cleaned_data['texto_pesquisado']
        try:
            item_pesquisado_id = int(self.cleaned_data['texto_pesquisado'])
        except:
            item_pesquisado_id = None

        self.resultados.queryset = ItemEmprestimo.objects.filter(
            Q(nome__icontains=item_pesquisado_texto) | Q(id=item_pesquisado_id))
