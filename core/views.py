from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
import logging
from .models import Categoria, FluxoDeCaixa as FC 


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
        tipos = [FC.TIPOS.renda[0], FC.TIPOS.despesa[0]]
        sub_tipos = [FC.TIPOS.variavel[0], FC.TIPOS.fixa[0]]

        ctx['usuario'] = usuario

        for tipo in tipos:
            ctx[f'{tipo}_total'] = self.soma_total(usuario, tipo=tipo)
            for sub_tipo in sub_tipos:
                ctx[f"{tipo}_{sub_tipo}"] = self.soma_total(usuario,tipo=tipo,sub_tipo=sub_tipo)       
        
        return render(request, self.template_name, ctx)

