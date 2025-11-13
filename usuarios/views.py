from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from .forms import LoginForm, RecuperarForm
from .models import Usuario, CodigoRecuperacion
import random

#  LoginView 
class LoginView(FormView):
    template_name = 'usuarios/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = Usuario.objects.filter(username=username).first()

        if user:
            if user.bloqueado:
                return self.render_to_response(self.get_context_data(form=form, mensaje='Cuenta bloqueada', alerta=True))
            elif user.password == password:
                user.intentos_fallidos = 0
                user.save()
                return redirect('bienvenida', username=user.username)
            else:
                user.intentos_fallidos += 1
                if user.intentos_fallidos >= 3:
                    user.bloqueado = True
                user.save()
                return self.render_to_response(self.get_context_data(form=form, mensaje='Credenciales incorrectas'))
        else:
            return self.render_to_response(self.get_context_data(form=form, mensaje='Usuario no encontrado'))

# RecuperarView 
class RecuperarView(FormView):
    template_name = 'usuarios/recuperar.html'
    form_class = RecuperarForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        user = Usuario.objects.filter(username=username).first()
        codigo = None

        if user:
            codigo = str(random.randint(100000, 999999))
            CodigoRecuperacion.objects.create(usuario=user, codigo=codigo)

        return self.render_to_response(self.get_context_data(form=form, codigo=codigo))

# BienvenidaView 
class BienvenidaView(DetailView):
    model = Usuario
    template_name = 'usuarios/bienvenida.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

# EditarUsuarioView 
class EditarUsuarioView(UpdateView):
    model = Usuario
    fields = ['password']
    template_name = 'usuarios/editar.html'

    def get_success_url(self):
        return redirect('bienvenida', username=self.object.username).url
