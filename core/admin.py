from django.contrib import admin
from .models import Pessoa, Emprestimo, ItemEmprestimo

admin.site.register(Pessoa)
admin.site.register(ItemEmprestimo)
admin.site.register(Emprestimo)
