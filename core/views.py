from django.shortcuts import render
from django.http import HttpResponse
from core.models import Pessoa, ItemEmprestimo
from django.db.models import Q
import json
from .forms import BuscaForm, ReservaForm


def pagina_busca(request):
    return render(request, 'pagina_busca.html', context=locals())


def resultado_busca(request):
    form = BuscaForm(request.GET)
    response = {}
    if form.is_valid():
        response = form.fazer_busca()
    return HttpResponse(json.dumps(response), content_type="application/json")




def fazer_reserva(request):
    form = ReservaForm(request.POST)
    response = {}
    if form.is_valid():        
        response = form.fazer_reserva()
    
    return HttpResponse(json.dumps(response), content_type="application/json")
