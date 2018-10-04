from core import views
from django.urls import path

urlpatterns = [
    #path('', views.index),
    path('emprestimos/', views.emprestimos, name='emprestimos'),
]
