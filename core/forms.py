from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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
