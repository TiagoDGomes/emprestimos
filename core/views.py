from django.shortcuts import render
from django.http.response import HttpResponse
from django.core import serializers
import json
from .models import Pessoa, ItemEmprestimo


def emprestimos(request):
    if 'p' in request.GET:
        pessoa_pesquisada = request.GET['p']
    if 'ip' in request.GET:
        item_pesquisado_texto = request.GET['ip']  
        if len(item_pesquisado_texto) >= 1:  
            itens_pesquisados = ItemEmprestimo.objects.filter(nome__icontains=item_pesquisado_texto)
            print(itens_pesquisados)
    return render(request, 'emprestimos.html', context=locals()) 


def busca(request):
    pass


def pessoa_json(request):
    pessoas = Pessoa.objects.filter(nome__contains=request.GET['palavra[term]'])
    result_json = serializers.serialize('json', pessoas)
    return HttpResponse(result_json)