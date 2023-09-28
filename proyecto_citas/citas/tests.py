import json
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from rest_framework.test import APITestCase

from .factories import CategoriaFactory
from .factories import ServicioFactory
from .factories import EstilistaFactory
from .factories import RolFactory
from .models import Categoria
from .models import Estilista
from .models import Servicio
from .models import Reserva


class CategoriaListCase(APITestCase):
    def setUp(self):
        self.categoria = CategoriaFactory()
        self.servicio = ServicioFactory()
        self.estilista = EstilistaFactory()

        self.servicio.estilistas.add(self.estilista)
        self.servicio.save()

    def make_request(self):
        """Request GET para obtener informacion de categorias"""
        return self.client.get(
            reverse(
                'citas:categoria-list'
            )
        )

    def test_exitoso_obteniendo_categorias_request(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 200)

        categorias = Categoria.objects.all()
        categoria = categorias.first()
        
        response_data = response.json()
        self.assertEqual(len(response_data['categorias']), categorias.count())
        self.assertEqual(
            response_data['categorias'][0]['nombre'], categoria.nombre
        )


class ServicioEstilistasListCase(APITestCase):
    def setUp(self):
        self.categoria = CategoriaFactory()
        self.servicio = ServicioFactory(
            categoria=self.categoria
        )
        self.estilista = EstilistaFactory()

        self.servicio.estilistas.add(self.estilista)
        self.servicio.save()

    def make_request(self):
        """Request GET para obtener Estilistas de un servicio"""
        return self.client.get(
            reverse(
                'citas:servicio-estilistas-list',
                args=[self.servicio.token_service]
            )
        )

    def test_exitoso_estilistas_por_servicio(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 200)

        servicio = Servicio.objects.get(token_service=self.servicio.token_service)
        estilistas = servicio.estilistas.all()

        estilista = Estilista.objects.get(email=estilistas.first().email)
        
        response_data = response.json()
        self.assertEqual(len(response_data['estilistas']), estilistas.count())
        self.assertEqual(response_data['estilistas'][0]['nombre'], 
            f"{estilista.nombre} {estilista.apellidos}"
        )


class CrearReservaCase(APITestCase):
    def setUp(self):
        self.rol = RolFactory()
        self.categoria = CategoriaFactory()
        self.servicio = ServicioFactory(
            categoria=self.categoria
        )
        self.estilista = EstilistaFactory()
        self.servicio.estilistas.add(self.estilista)
        self.servicio.save()

    def boby_request(self):
        return{
            'servicio':self.servicio.token_service,
            'estilista':self.estilista.email,
            'cliente': 'vane.hoyos@gmail.com',
            'fecha': "2023-09-01",
            'hora_inicio': "10:00",
            'hora_fin': "11:00"
        }

    def make_request(self, data):
        """Request POST para crear reserva"""
        return self.client.post(
            reverse(
                'citas:crear-reserva'
            ),
            data=data
        )

    def test_crear_reserva(self):
        numero_de_reservas = Reserva.objects.all().count()
        self.assertEqual(numero_de_reservas, 0)

        body_request = self.boby_request()
        response = self.make_request(body_request)
        self.assertEqual(response.status_code, 201)

        reserva=Reserva.objects.all().first()
        
        response_data = response.json()
        self.assertEqual(response_data['cliente'], reserva.cliente.id)
        self.assertEqual(response_data['servicio'], reserva.servicio.id)
        self.assertEqual(response_data['estilista'], reserva.estilista.id)
        self.assertEqual(response_data['fecha'], body_request['fecha'])
        self.assertEqual(response_data['hora_inicio'], body_request['hora_inicio'])
        self.assertEqual(response_data['hora_fin'], body_request['hora_fin'])
