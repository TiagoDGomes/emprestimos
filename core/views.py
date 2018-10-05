from django.shortcuts import render
from django.http.response import HttpResponse
from django.core import serializers
from django.db.models.query import Q
import json
from .models import Pessoa, ItemEmprestimo



def emprestimos(request):
    if 'p' in request.GET:
        try:
            pessoa_pesquisada_id = int(request.GET['p'])
            pessoa_pesquisada = Pessoa.objects.get(id=pessoa_pesquisada_id)
        except:
            pass
        
    if 'ip' in request.GET:
        item_pesquisado_texto = request.GET['ip']  
        try:
            item_pesquisado_id = int(item_pesquisado_texto)
        except:
            item_pesquisado_id = None
        if len(item_pesquisado_texto) >= 1: 

            try:
                hps = request.GET['h'].split(',')
            except:
                hps = []
            historico_pesquisa = list(map(int, filter(None,hps) ))

                
            #try:
            itens_da_pesquisa = ItemEmprestimo.objects.filter(Q(nome__icontains=item_pesquisado_texto)|Q(id=item_pesquisado_id))
            if len(itens_da_pesquisa) == 1:
                itens_da_pesquisa = None
                itens_historico_pesquisa = ItemEmprestimo.objects.filter(Q(id__in=historico_pesquisa)|Q(id=item_pesquisado_id))
                historico_pesquisa.append(item_pesquisado_id)
            else:
                itens_historico_pesquisa = ItemEmprestimo.objects.filter(id__in=historico_pesquisa)
            
            historico_pesquisa_texto = ','.join(hps)
            print(historico_pesquisa)

            
            
            
    return render(request, 'emprestimos.html', context=locals()) 


def busca(request):
    pass


def pessoa_json(request):
    pessoas = Pessoa.objects.filter(nome__contains=request.GET['palavra[term]'])
    result_json = serializers.serialize('json', pessoas)
    return HttpResponse(result_json)