import logging

from concurrency.exceptions import RecordModifiedError
from datetime import datetime
from datetime import timedelta

from .models import Cliente
from .models import Estilista
from .models import Servicio
from .models import Reserva
from .models import Rol
from .models import Horario

from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def crear_reserva(servicio, estilista, cliente, fecha, hora_inicio, hora_fin):
    try:
        cliente = Cliente.objects.get(email=cliente)
    except Cliente.DoesNotExist:
        rol_cliente = Rol.objects.get(tipo_rol='cliente')

        cliente = Cliente(
            email=cliente
        )

        cliente.save()

        cliente.roles.add(rol_cliente)

    try:
        estilista = Estilista.objects.get(email=estilista)
    except Estilista.DoesNotExist:
        return('No se encontro estilista', False)
    
    try:
        servicio = Servicio.objects.get(token_service=servicio)
    except Servicio.DoesNotExist:
        return('No se encontro servicio', False)

    reserva = Reserva(
        servicio=servicio,
        estilista=estilista,
        cliente=cliente,
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin
    )

    try:
        reserva.validate_unique()
    except ValidationError:
        reserva = Reserva.objects.get(
            servicio=servicio,
            estilista=estilista,
            cliente=cliente,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )

        return (reserva, False)

    
    reserva.save()
    
    return(reserva, True)

def reabrir_turno(hora_inicio, hora_fin, fecha, estilista):
    try:
        horario = Horario.objects.get(
            estilista=estilista,
            fecha=fecha,
            hora_inicio__lte=hora_inicio,
            hora_fin__gte=hora_fin
        )
    except Horario.DoesNotExist:
        return False

    # Convierte los objetos TimeField en objetos datetime.time
    hora_inicio = hora_inicio.replace(second=0, microsecond=0)
    hora_fin = hora_fin.replace(second=0, microsecond=0)

    # Calcula la diferencia de tiempo entre la hora de inicio y la hora de fin
    diferencia = datetime.combine(datetime.today(), hora_fin) - datetime.combine(
        datetime.today(), hora_inicio)

    # Calcula el número de minutos totales
    minutos_totales = int(diferencia.total_seconds() / 60)

    horario.horarios.append(hora_inicio)
    # Calcula las horas intermedias y agrégalas a una lista en formato "hh:mm"
    if (minutos_totales // 60) == 1:
        for i in range(minutos_totales // 60):
            hora_intermedia = hora_inicio + timedelta(hours=i)
            horario.horarios.append(hora_intermedia.strftime('%H:%M'))
    
    horario.save()

    return True


def modificar_reserva(token, fecha, hora_inicio, hora_fin):
    try:
        reserva=Reserva.objects.get(token_service=token)
    except Reserva.DoesNotExist:
        return {'message': f"Reserva {token} no existe"}, False

    try:
        estilista=Estilista.objects.get(id=reserva.estilista.id)
    except Estilista.DoesNotExist:
        return {'message': f"El estilista {reserva.estilista.nombre} ya no existe en el salid de belleza"}, False

    try:
        orig_status = reserva.estado
        reserva.estado = 'Reprogramada'
        reserva.save()
    except RecordModifiedError:
        reserva.estado = orig_status
        logger.warning(
            ('Error al intentar modificar estado contra la Base de datos'),
            extra=dict(reserva=reserva.token_service)
        )
        return {'message': "No se pudo realizar la modificacion intentelo mas tarde"}, False

    nueva_reserva = Reserva(
        servicio=reserva.servicio,
        estilista=estilista,
        cliente=reserva.cliente,
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin
    )

    try:
        nueva_reserva.validate_unique()
    except ValidationError:
        nueva_reserva = Reserva.objects.get(
            servicio=reserva.servicio,
            estilista=estilista,
            cliente=reserva.cliente,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        logger.warning(
            ('reserva ya existe'),
            extra=dict(reserva=nueva_reserva.token_service)
        )
        return (nueva_reserva, True)

    abrir_turno = reabrir_turno(
        hora_inicio=reserva.hora_inicio,
        hora_fin=reserva.hora_fin,
        fecha=reserva.fecha,
        estilista=estilista
    )

    if not abrir_turno:
        logger.warning(
            ('Error al intentar modificar estado contra la Base de datos'),
            extra=dict(reserva=reserva.token_service)
        )

    return nueva_reserva, True

def cancelar_reserva(token):
    try:
        reserva=Reserva.objects.get(token_service=token)
    except Reserva.DoesNotExist:
        return {'message': f"Reserva {token} no existe"}, False
    
    try:
        orig_status = reserva.estado
        reserva.estado = 'Cancelada'
        reserva.save()
    except RecordModifiedError:
        reserva.estado = orig_status
        logger.warning(
            ('Error al intentar cancelar la reserva modificando el estado'),
            extra=dict(reserva=reserva.token_service)
        )
        return {'message': "No se pudo realizar la cancelacion intentelo mas tarde"}, False

    return reserva, True
