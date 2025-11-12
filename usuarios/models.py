from django.db import models

class Usuario(models.Model):
    CARGOS_VALIDOS = [
        ('medico', 'Medico'),
        ('matron', 'Matron/a'),
        ('enfermero', 'Enfermero/a'),
        ('admin', 'Administrativo'),
    ]
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    cargo = models.CharField(max_length=20, choices=CARGOS_VALIDOS)
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.cargo})"

class CodigoRecuperacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    creado = models.DateTimeField(auto_now_add=True)
