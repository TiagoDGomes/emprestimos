from core import views
from django.urls import path

urlpatterns = [
    #path('', views.index),
    path('busca/', views.pagina_busca, name='pagina_busca'),
]
