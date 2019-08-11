from core import views
from django.urls import path


urlpatterns = [
    #path('', views.index),
    path('busca/', views.pagina_busca, name='pagina_busca'),
    path('resultado.json', views.resultado_busca, name='resultado_busca'),
    path('fazer_reserva/', views.fazer_reserva, name='fazer_reserva'),
]
