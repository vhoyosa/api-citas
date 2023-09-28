from collections import namedtuple

from common.views import ServiceView

from rest_framework import status
from rest_framework.response import Response

from .models import Categoria
from .models import Servicio
from .models import Horario
from .models import Reserva
from .serializers import NoDataSerializer
from .serializers import CategoriasYServiciosListaResponseSerializer
from .serializers import ReservaResponseSerializer
from .services import crear_reserva
from .services import modificar_reserva
from .services import cancelar_reserva


class CategoriaListView(ServiceView):
    http_method = 'GET'
    request_serializer = NoDataSerializer
    response_serializer = CategoriasYServiciosListaResponseSerializer

    def process_request(self, request_serializer_obj, request):
        obj = namedtuple(
            'CategoriasLista',
            ['categorias'],
        )(Categoria.objects.all())

        if not obj:
            return Response(status=status.HTTP_409_CONFLICT)

        return obj, status.HTTP_200_OK


class ServicioEstilistasListView(ServiceView):
    http_method = 'GET'
    request_serializer = NoDataSerializer
    response_serializer = NoDataSerializer

    def process_request(self, request_serializer_obj, request):
        token = self.kwargs['token_servicio']

        obj = Servicio.objects.filter(token_service=token)

        if not obj:
            return Response(status=status.HTTP_409_CONFLICT)

        body_principal = {
            "estilistas" : []
        }

        for estilista in obj.first().estilistas.all():
            body_complementario = {
                "nombre": "Ana",
                "dias":[]
            }

            body_complementario['nombre'] = f"{estilista.nombre} {estilista.apellidos}"
            body_complementario['email'] =  estilista.email

            obj_horarios = Horario.objects.filter(estilista=estilista)

            for horario in obj_horarios:
                body_horarios = {
                    "fecha": "2",
                }
                body_horarios['fecha'] = horario.fecha
                body_horarios['horarios'] = horario.horarios

                body_complementario['dias'].append(body_horarios)
            
            body_principal['estilistas'].append(body_complementario)

        return Response(body_principal, status=status.HTTP_200_OK)


class CrearReservaView(ServiceView):
    http_method = 'POST'
    request_serializer = NoDataSerializer
    response_serializer = ReservaResponseSerializer

    def process_request(self, request_serializer_obj, request):

        data = request.data
        
        obj_reserva, status_request = crear_reserva(
            servicio=data['servicio'],
            estilista=data['estilista'],
            cliente=data['cliente'],
            fecha=data['fecha'],
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin']
        )

        if not status_request or not isinstance(obj_reserva, Reserva):
            return Response(status=status.HTTP_409_CONFLICT)

        if status_request:
            return obj_reserva, status.HTTP_201_CREATED

        return Response(status.HTTP_503_SERVICE_UNAVAILABLE)


class ListarReservasView(ServiceView):
    http_method = 'GET'
    request_serializer = NoDataSerializer
    response_serializer = NoDataSerializer

    def process_request(self, request_serializer_obj, request):
        data = request.data
        objects_reservas = Reserva.objects.filter(cliente=data['cliente'])

        if not objects_reservas:
            return Response([], status=status.HTTP_200_OK)

        serializer = ReservaResponseSerializer(objects_reservas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ModificarReservaView(ServiceView):
    http_method = 'POST'
    request_serializer = NoDataSerializer
    response_serializer = ReservaResponseSerializer

    def process_request(self, request_serializer_obj, request):

        data = request.data
        
        obj_reserva, status_request = modificar_reserva(
            toke=data['token'],
            fecha=data['fecha'],
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin']
        )

        if not isinstance(obj_reserva, Reserva):
            return Response(obj_reserva, status=status.HTTP_409_CONFLICT)

        if status_request:
            return obj_reserva, status.HTTP_201_CREATED

        return Response(status.HTTP_503_SERVICE_UNAVAILABLE)


class CancelarReserva(ServiceView):
    http_method = 'POST'
    request_serializer = NoDataSerializer
    response_serializer = ReservaResponseSerializer

    def process_request(self, request_serializer_obj, request):

        data = request.data
        
        obj_reserva, status_request = cancelar_reserva(
            toke=data['token']
        )

        if not isinstance(obj_reserva, Reserva):
            return Response(status=status.HTTP_409_CONFLICT)

        if status_request:
            return obj_reserva, status.status.HTTP_200_OK

        return Response(status.HTTP_503_SERVICE_UNAVAILABLE)
