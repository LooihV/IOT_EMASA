from rest_framework import serializers
from .models import Programador
from .models import Machine, Registro
from .models import User, CustomUser
from django.contrib.auth import get_user_model


class ProgrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programador
        fields='__all__'







class MachineSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username',read_only =True)
    class Meta:
        model = Machine
        fields='__all__'


class RegistroSerializer(serializers.ModelSerializer):

    maquina = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.none()  # Inicialmente vacío, lo llenaremos en _init_
    )

    def __init__(self, *args, **kwargs):
        super(RegistroSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)  # Obtener la solicitud
        
        if request and request.user.is_authenticated:  # Verificar si el usuario está autenticado
            user = request.user
            if user.is_superuser:  # Si es admin, mostrar todas las máquinas
                self.fields['maquina'].queryset = Machine.objects.all()
            else:  # Si no, filtrar solo las máquinas relacionadas a él
                self.fields['maquina'].queryset = Machine.objects.filter(user=user)

    class Meta:
        model = Registro
        fields='__all__'



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])  # Encripta la contraseña
        user.save()
        return user