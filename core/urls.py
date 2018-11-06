from core import views
from django.urls import path

urlpatterns = [
    #path('', views.index),
    path('emprestimos/', views.emprestimos, name='emprestimos'),
    path('colocar_no_historico_atual/', views.colocar_no_historico, name='colocar_no_historico_atual'),
    path('pessoa_json/', views.pessoa_json, name='pessoa_json'),
]
