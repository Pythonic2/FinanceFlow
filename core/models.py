from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Método para criar categorias padrão ao criar um novo usuário
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            CategoriaDespesa.objects.create(usuario=self, nome='Despesas Fixas')
            CategoriaDespesa.objects.create(usuario=self, nome='Despesas Variaveis')
            CategoriaRenda.objects.create(usuario=self, nome='Salário')
            CategoriaRenda.objects.create(usuario=self, nome='Renda Extra')

class CategoriaDespesa(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Despesa(models.Model):
    categoria = models.ForeignKey(CategoriaDespesa, on_delete=models.CASCADE, related_name='despesas')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    descricao = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.categoria.nome} - {self.valor} em {self.data}"

class CategoriaRenda(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class Renda(models.Model):
    categoria = models.ForeignKey(CategoriaRenda, on_delete=models.CASCADE, related_name='rendas')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    descricao = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
