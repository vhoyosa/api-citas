from rest_framework import serializers
from .models import Categoria, Servicio, Horario, Estilista, Reserva

class ServicioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=False)
    class Meta:
        model = Servicio
        fields = ('nombre', 'descripcion', 'precio', 'token_service')


class CategoriaSerializer(serializers.ModelSerializer):
    servicios = ServicioSerializer(many=True, required=False)

    class Meta:
        model = Categoria
        fields = ('id', 'nombre', 'descripcion', 'servicios')


class CategoriasYServiciosListaResponseSerializer(serializers.Serializer):
    categorias = CategoriaSerializer(many=True)


class NoDataSerializer(serializers.Serializer):
    pass


class ReservaResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = "__all__"
