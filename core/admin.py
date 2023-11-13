from django.contrib import admin

# Register your models here.
from core.models import CustomUser, CategoriaDespesa, Despesa, CategoriaRenda, Renda

admin.site.register(CustomUser)
admin.site.register(CategoriaDespesa)
admin.site.register(Despesa)
admin.site.register(CategoriaRenda)
admin.site.register(Renda)