from django.contrib import admin

# Register your models here.
from core.models import CustomUser, FluxoDeCaixa, Categoria

admin.site.register(CustomUser)
admin.site.register(FluxoDeCaixa)
admin.site.register(Categoria)