from rest_framework import serializers
from .models import Programador
from .models import Machine, Registro
from .models import User, CustomUser
from django.contrib.auth import get_user_model
#from .chirpstack_api import create_user_in_chirpstack, update_user_in_chirpstack, delete_user_in_chirpstack

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

    machine = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.none()  
    )

    def __init__(self, *args, **kwargs):
        super(RegistroSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)  
        
        if request and request.user.is_authenticated: 
            user = request.user
            if user.is_superuser:  
                self.fields['machine'].queryset = Machine.objects.all()
            else:  # Si no, filtrar solo las máquinas relacionadas a él
                self.fields['machine'].queryset = Machine.objects.filter(user=user)

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
            email=validated_data.get('email', ''),
            is_superuser=validated_data.get('is_superuser',False),
            is_staff=validated_data.get('is_staff',False)

        )
        user.set_password(validated_data['password'])  
        user.save()
        
        from api.chirpstack_api import sync_user_to_chirpstack 
        sync_user_to_chirpstack(sender=User, instance=user, created=True)
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  
            validated_data.pop('password')  
        return super().update(instance, validated_data)
    