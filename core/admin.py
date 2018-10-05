from django.contrib import admin
from .models import Pessoa, Emprestimo, TipoItem, ItemEmprestimo

admin.site.register(Pessoa)
admin.site.register(TipoItem)
admin.site.register(ItemEmprestimo)
admin.site.register(Emprestimo)
