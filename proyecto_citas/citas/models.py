from django.db import models
from django.contrib.postgres.fields import ArrayField
from functools import partial

from common.utils import generate_token

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()


class Estilista(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    celular = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, db_index=True, unique=True)


class Servicio(models.Model):
    token_service = models.CharField(
        unique=True,
        default=partial(generate_token, 'srv'),
        max_length=32,
    )
    categoria = models.ForeignKey(Categoria, related_name='servicios', on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estilistas = models.ManyToManyField(Estilista, related_name='servicios_realizados', null=True, blank=True)


class Horario(models.Model):
    estilista = models.ForeignKey(Estilista, related_name='horarios', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField() #hora de inicio turno de trabajo
    hora_fin = models.TimeField() #hora de fin turno de trabajo
    horarios = ArrayField(models.TimeField()) #horarios disponibles en el turno
    created_at = models.DateTimeField(
        verbose_name='creación',
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='actualización',
        auto_now=True,
        db_index=True,
    )


class Rol(models.Model):
    tipo_rol = models.CharField(max_length=255, choices=[('cliente', 'cliente'), ('admin', 'admin')], unique=True)


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    roles = models.ManyToManyField(Rol, related_name='roles_asignados')


class Reserva(models.Model):
    token_service = models.CharField(
        unique=True,
        default=partial(generate_token, 'res'),
        max_length=32,
    )
    estado = models.CharField(
        max_length=255,
        choices=[
            ('Programada', 'Programada'),
            ('Reprogramada', 'Reprogramada'),
            ('No Asistió', 'No Asistió'),
            ('Cancelada', 'Cancelada'),
            ('Confirmada', 'Confirmada')
        ],
        default='Programada'
    )
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estilista = models.ForeignKey(Estilista, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('servicio', 'estilista', 'cliente', 'fecha', 'hora_inicio', 'hora_fin')
