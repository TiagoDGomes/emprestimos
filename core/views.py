from django.shortcuts import render
def pagina_busca(request):
    return render(request, 'pagina_busca.html', context=locals()) 