from django.urls import path
from .views import LoginView, RecuperarView, BienvenidaView, EditarUsuarioView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('recuperar/', RecuperarView.as_view(), name='recuperar'),
    path('bienvenida/<slug:username>/', BienvenidaView.as_view(), name='bienvenida'),
    path('editar/<int:pk>/', EditarUsuarioView.as_view(), name='editar'),
]
