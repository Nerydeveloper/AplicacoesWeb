from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Categoria)
admin.site.register(Mercado)
admin.site.register(Produto)
admin.site.register(Lista)
admin.site.register(Receita)

