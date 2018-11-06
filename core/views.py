from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.db.models.query import Q
import json
from .models import Pessoa, ItemEmprestimo
from .forms import PesquisaEmprestimoForm

def split_historico(txt):
    hps = txt.split(',')
    hps = [e for e in hps if e.upper() != 'NONE']  
    print(('hps3', hps))
    hps = list(map(int, hps)) 
    print(('hps1', hps))
    hps = [e for e in hps if isinstance(e, int)]  
    print(('hps2', hps))
    hps = filter(None, hps) 
    print(('hps4', hps))
    hps = list(set(hps))  
    print(('hps5', hps))
    return hps



def colocar_no_historico(request):
    pessoa_pesquisada_id = ""
    item_pesquisado_texto = ""
    historico = ""
    try:
        pessoa_pesquisada_id = request.GET['p']
        #item_pesquisado_texto = request.GET['ip'] 
        try:
            historico_pesquisa = split_historico(request.GET['h']) 
        except Exception as e:
            historico_pesquisa = []     
        for g in request.GET:
            kv = g.split('-')
            if kv[0] == 'it':
                historico_pesquisa.append(kv[1])
        historico_pesquisa_texto = ','.join(str(x) for x in historico_pesquisa) 
    except:
        pass
    return HttpResponseRedirect("{url}?p={p}&h={h}".format(
                            url=reverse('emprestimos'),
                            p=pessoa_pesquisada_id,
                            ip=item_pesquisado_texto,
                            h=historico_pesquisa_texto,
                            ))


def emprestimos(request):
    if 'p' in request.GET:
        try:
            pessoa_pesquisada_id = int(request.GET['p'])
            pessoa_pesquisada = Pessoa.objects.get(id=pessoa_pesquisada_id)
        except:
            pass
        
    if 'ip' in request.GET:
        item_pesquisado_texto = request.GET['ip']  
        #print(('item_pesquisado_texto',item_pesquisado_texto))
        #print(('h',item_pesquisado_texto))
    else:
        item_pesquisado_texto = ""    
    try:
        item_pesquisado_id = int(item_pesquisado_texto)
    except:
        item_pesquisado_id = None
    
    try:
        historico_pesquisa = split_historico(request.GET['h']) 
    except Exception as e:
        historico_pesquisa = []   

    if len(item_pesquisado_texto)> 1:       
        itens_da_pesquisa = ItemEmprestimo.objects.filter(Q(nome__icontains=item_pesquisado_texto)|Q(id=item_pesquisado_id))
    else:
        itens_da_pesquisa = ItemEmprestimo.objects.filter(id=item_pesquisado_id)

    if len(itens_da_pesquisa) == 1:
        itens_da_pesquisa = None
        itens_historico_pesquisa = ItemEmprestimo.objects.filter(Q(id__in=historico_pesquisa)|Q(id=item_pesquisado_id))
        historico_pesquisa.append(item_pesquisado_id)
        historico_pesquisa = list(set(historico_pesquisa))
    else:
        itens_historico_pesquisa = ItemEmprestimo.objects.filter(id__in=historico_pesquisa)
    historico_pesquisa_texto = ','.join(str(x) for x in historico_pesquisa) 
            
    return render(request, 'emprestimos.html', context=locals()) 



def pessoa_json(request):
    pessoas = Pessoa.objects.filter(nome__contains=request.GET['palavra[term]'])
    result_json = serializers.serialize('json', pessoas)
    return HttpResponse(result_json)