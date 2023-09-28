from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^categorias$',
        views.CategoriaListView.as_view(),
        name='categoria-list',
    ),
    url(
        r'^servicios/(?P<token_servicio>[-\w]+)/estilistas$',
        views.ServicioEstilistasListView.as_view(),
        name='servicio-estilistas-list',
    ),
    url(
        r'^reserva$',
        views.CrearReservaView.as_view(),
        name='crear-reserva',
    ),
    url(
        r'^reserva/mis-reservas$',
        views.ListarReservasView.as_view(),
        name='historial-reservas',
    ),
    url(
        r'^reserva/reprogramar$',
        views.ModificarReservaView.as_view(),
        name='reprogramar-reservas',
    ),
    url(
        r'^reserva/cancelar$',
        views.CancelarReserva.as_view(),
        name='cancelar-reservas',
    )
]
