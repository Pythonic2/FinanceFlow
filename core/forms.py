from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Categoria, FluxoDeCaixa

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Confirme a Senha'})

        self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres.'
        self.fields['password2'].help_text = 'Repita a senha para verificação.'

        # Personalizar os widgets conforme necessário
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control form-control-user'})

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Nome'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Descrição'})

class FluxoDeCaixaForm(forms.ModelForm):
    class Meta:
        model = FluxoDeCaixa
        fields = ['tipo', 'sub_tipo', 'categoria', 'valor', 'data', 'paga','necessidade']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FluxoDeCaixaForm, self).__init__(*args, **kwargs)
        # Configuração dos widgets
        self.fields['tipo'].widget.attrs.update({'class': 'form-control form-control-user'})
        self.fields['sub_tipo'].widget.attrs.update({'class': 'form-control form-control-user'})
        if user is not None:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
        self.fields['categoria'].widget.attrs.update({'class': 'form-control form-control-user'})
        self.fields['necessidade'].widget.attrs.update({'class': 'form-control form-control-user'})
        self.fields['valor'].widget.attrs.update({'class': 'form-control form-control-user', 'step': '0.01'})
        self.fields['data'].widget.attrs.update({'class': 'form-control form-control-user', 'type': 'date'})
        self.fields['paga'].widget.attrs.update({'class': 'form-check-input'})
        self.fields.pop('usuario', None)