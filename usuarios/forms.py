from django import forms
from .models import Usuario

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class RecuperarForm(forms.Form):
    username = forms.CharField(label='Usuario')

    def clean_username(self):
        username = self.cleaned_data['username']
        user = Usuario.objects.filter(username=username).first()

        if not user:
            raise forms.ValidationError('Usuario no encontrado.')

        if user.bloqueado:
            raise forms.ValidationError('La cuenta está bloqueada. No se puede recuperar.')

        return username