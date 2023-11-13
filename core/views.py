from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Renda, Despesa
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
import logging
from .models import CategoriaRenda, CategoriaDespesa


logger = logging.getLogger(__name__)
from django.contrib.auth import user_logged_in

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        user_exists = User.objects.filter(username=username).exists()

        if not user_exists:
            messages.error(self.request, 'Usuário não cadastrado.')
        else:
            messages.error(self.request, 'Usuário ou senha incorretos.')

        return super().form_invalid(form)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cadastro realizado com sucesso. Por favor, faça o login.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erro no cadastro. Por favor, verifique os dados informados.')
        return super().form_invalid(form)


        
class Index(TemplateView):
    template_name = 'index.html'

    def soma_total_despesas(self, usuario):
        return Despesa.objects.filter(usuario=usuario).aggregate(soma_total=Sum('valor'))['soma_total'] or 0

    def soma_total_rendas(self, usuario):
        return Renda.objects.filter(usuario=usuario).aggregate(soma_total=Sum('valor'))['soma_total'] or 0

    def get(self, request, *args, **kwargs):
        renda_total = self.soma_total_rendas(request.user)
        despesa_total = self.soma_total_despesas(request.user)
        
        usuario_logado = request.user
        
        if usuario_logado.is_authenticated:
            print(f"Usuário logado: {usuario_logado.username}") 
        else:
            print("Nenhum usuário logado")
            
        
        categorias_renda = CategoriaRenda.objects.filter(
            usuario=request.user,
            nome__in=['Salário', 'Renda Extra']
        )

        # Filtra as categorias de despesa específicas
        categorias_despesa = CategoriaDespesa.objects.filter(
            usuario=request.user,
            nome__in=['Despesas Fixas', 'Despesas Variáveis']
        )
        for cat in categorias_renda:
            print(cat.nome)
        
        return render(request, self.template_name, {'usuario':usuario_logado.username,'renda_total': renda_total, 'despesa_total': despesa_total, 'categoria_renda':categorias_renda,'categoria_despesa':categorias_despesa})

