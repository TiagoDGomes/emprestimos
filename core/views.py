from django.shortcuts import render
from django.http import HttpResponse
from core.models import Pessoa, ItemEmprestimo
from django.db.models import Q
import json


def pagina_busca(request):
    return render(request, 'pagina_busca.html', context=locals())


def resultado_busca(request):
    response = {}
    try:
        texto = request.GET['texto']
        if texto != '':
            pesquisa_pessoa = [{'nome': x.nome,
                                'matricula': x.matricula,
                                'detalhes': x.detalhes,
                                'observacao': x.observacao,
                                'bloqueio': x.bloqueio}
                               for x in Pessoa.objects.filter(Q(nome__contains=texto) |
                                                              Q(matricula=texto) |
                                                              Q(cpf=texto))]
            pesquisa_itens = [{'codigo': x.codigo,
                               'nome': x.nome,
                               'status': x.status}
                              for x in ItemEmprestimo.objects.filter(Q(nome__contains=texto) |
                                                                     Q(palavras_chave__contains=texto) |
                                                                     Q(codigo__contains=texto))]
            response = dict(texto=texto,
                            pessoas=pesquisa_pessoa,
                            itens=pesquisa_itens)
    except KeyError:
        pass
    return HttpResponse(json.dumps(response), content_type="application/json")
