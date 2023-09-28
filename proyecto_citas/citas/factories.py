import factory

from decimal import Decimal

from factory.django import DjangoModelFactory

from .models import Categoria
from .models import Estilista
from .models import Servicio
from .models import Horario
from .models import Rol


class CategoriaFactory(DjangoModelFactory):
    nombre="Arrego de Uñas"
    descripcion="Arreglo de uñas de manos y Pies"

    class Meta:
        model = Categoria


class EstilistaFactory(DjangoModelFactory):
    nombre="Vanessa"
    apellidos="Hoyos Arenas"
    celular="+573014866556"
    email="uncorreo@gmail.com"

    class Meta:
        model = Estilista


class ServicioFactory(DjangoModelFactory):
    nombre="Tradicional-manos"
    descripcion="Arreglo de uñas clasico, sin mañor decoracion"
    precio=Decimal("17000")
    categoria=factory.SubFactory(
        CategoriaFactory,
    )

    class Meta:
        model = Servicio

class HorarioFactory(DjangoModelFactory):
    from factory import Faker
    from datetime import datetime

    estilista = factory.SubFactory(EstilistaFactory)
    fecha = factory.Faker('date_time_between_dates', datetime_start=datetime(2023, 9, 1), datetime_end=datetime(2023, 9, 1))
    hora_inicio = factory.Faker('time', pattern='%H:%M:%S', end_datetime=None)
    hora_fin = factory.Faker('time', pattern='%H:%M:%S', end_datetime=None)
    horarios = [hora_inicio, hora_fin]

    class Meta:
        model = Horario

class RolFactory(DjangoModelFactory):
    tipo_rol='cliente'

    class Meta:
        model=Rol