from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from dataclasses import dataclass

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Método para criar categorias padrão ao criar um novo usuário
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)   


class FluxoDeCaixa(models.Model):
    @dataclass
    class TIPOS:
        fixa = ("fixa", "Fixa")
        variavel = ("variavel", "Variável")
        renda = ('renda', 'Renda')
        despesa = ('despesa', 'Despesa')

    _TIPOS = (TIPOS.renda, TIPOS.despesa)
    _SUB_TIPOS = (TIPOS.fixa, TIPOS.variavel)
    tipo = models.CharField(choices=_TIPOS, max_length=8)    
    sub_tipo = models.CharField(choices=_SUB_TIPOS, max_length=8)   
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    paga = models.BooleanField(default=False)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.valor} em {self.data}"
    

class Categoria(models.Model):    
    nome = models.CharField(max_length=100)    
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.descricao}"

    

