from typing import Any
from django import http
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,DeleteView, UpdateView
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
import logging
from .models import Categoria, FluxoDeCaixa as FC 
from .forms import CategoriaForm, FluxoDeCaixaForm
from django.utils import timezone
logger = logging.getLogger(__name__)
from django.contrib.auth import user_logged_in
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return redirect("login")
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


class SignUpView(CreateView):
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
    
    def soma_total(self, usuario, tipo:str, sub_tipo:str=None):
        if not sub_tipo:
            return FC.objects.filter(
                usuario=usuario, 
                tipo=tipo       
                ).aggregate(soma_total=Sum('valor'))['soma_total']
        return FC.objects.filter(
                usuario=usuario, 
                tipo=tipo,
                sub_tipo=sub_tipo
                ).aggregate(soma_total=Sum('valor'))['soma_total']
                
    
    def get(self, request, *args, **kwargs):
        ctx = {}
        usuario = request.user
        if usuario.is_authenticated:
            # Filtrar categorias pelo usuário logado
            categorias_usuario = Categoria.objects.filter(usuario=usuario)

            # Adicionar categorias ao contexto
            ctx['categorias'] = categorias_usuario
            tipos = [FC.TIPOS.renda[0], FC.TIPOS.despesa[0]]
            sub_tipos = [FC.TIPOS.variavel[0], FC.TIPOS.fixa[0]]
            
            ctx['usuario'] = usuario
            for tipo in tipos:
                ctx[f'{tipo}_total'] = self.soma_total(usuario, tipo=tipo)
                for sub_tipo in sub_tipos:
                    ctx[f"{tipo}_{sub_tipo}"] = self.soma_total(usuario,tipo=tipo,sub_tipo=sub_tipo)       
            ctx['form'] = CategoriaForm()
            ctx['fc'] = FluxoDeCaixaForm(user=usuario)
            ctx['titulo'] = 'Dashboard'
            count_nao_pagos = FC.objects.filter(usuario=usuario, paga=False, tipo='despesa').count()
            count_pagos = FC.objects.filter(usuario=usuario, paga=True, tipo='despesa').count()
            ctx['nao_pagos'] = count_nao_pagos
            ctx['pagos'] = count_pagos
            

            # ... (código anterior)

            despesas = FC.objects.filter(usuario=usuario, tipo='despesa')

            total_despesas = sum(fc.valor for fc in despesas)

            porcentagem_essenciais = 0
            porcentagem_desejos = 0
            porcentagem_investimentos = 0

            if total_despesas != 0:
                porcentagem_essenciais = (sum(fc.valor for fc in despesas.filter(necessidade='essencial')) / total_despesas) * 100
                porcentagem_desejos = (sum(fc.valor for fc in despesas.filter(necessidade='desejos')) / total_despesas) * 100
                porcentagem_investimentos = (sum(fc.valor for fc in despesas.filter(necessidade='investimentos')) / total_despesas) * 100
                ctx['porcentagem_essenciais'] = round(porcentagem_essenciais, 2)
                ctx['porcentagem_desejos'] = round(porcentagem_desejos, 2)
                ctx['porcentagem_investimentos'] = round(porcentagem_investimentos, 2)
            else:
                return redirect ('login')
        return render(request, self.template_name, ctx)

    
class NewFlux(CreateView):
    template_name = 'new_flux.html'
    form_class = FluxoDeCaixaForm
    success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super(NewFlux, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        fluxo_de_caixa = form.save(commit=False)
        fluxo_de_caixa.usuario = self.request.user
        fluxo_de_caixa.save()
        messages.success(self.request, 'Entrada/Saída cadastrada com sucesso.')
        return super(NewFlux, self).form_valid(form)


class NewCategory(CreateView):
    form_class = CategoriaForm
    template_name = 'new_category.html'
    success_url = reverse_lazy('category_list')
    
    def form_valid(self, form):
        categoria = form.save(commit=False)
        categoria.usuario = self.request.user  # Associando a categoria ao usuário logado
        categoria.save()
        messages.success(self.request, 'Categoria Cadastrada com Sucesso')
        return super().form_valid(form)
    

class ListCategory(ListView):
    model = Categoria
    template_name = 'categoria_list.html'
    def get_queryset(self) -> QuerySet[Any]:
        return Categoria.objects.filter(usuario=self.request.user)
    def get_context_data(self, **kwargs):
        # Chame a implementação base para obter um contexto
        context = super().get_context_data(**kwargs)
        # Adicione suas variáveis ao contexto
        context['titulo'] = 'Lista de Categorias'

        return context
   

class UpdateCategory(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria_edite.html'
    success_url = reverse_lazy('category_list')
    
class DeletCategory(DeleteView):
    model = Categoria
    success_url = reverse_lazy('category_list')
    template_name = 'categoria_confirm_delete.html'