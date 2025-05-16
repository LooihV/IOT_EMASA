from rest_framework import serializers
from .models import Machine, Registro, Tenant
from .models import  CustomUser #, User
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
#from .chirpstack_api import create_user_in_chirpstack, update_user_in_chirpstack, delete_user_in_chirpstack



class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
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
            else:  # de lo contarrio solo las máquinas relacionadas a él
                self.fields['machine'].queryset = Machine.objects.filter(user=user)

    class Meta:
        model = Registro
        fields='__all__'



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), required=False, allow_null=True)
    class Meta:
        model = User
        fields = '__all__'
    

    def create(self, validated_data):
        password = validated_data.get('password')
        tenant = validated_data.pop('tenant', None)
        
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            is_superuser=validated_data.get('is_superuser', False),
            is_staff=validated_data.get('is_staff', False),
            tenant=tenant,
        )
        user.set_password(password)  # Aquí usas el password bien
        user.save()

        send_mail(
            subject=f"MONITOR: Bienvenido {user.username}",
            message=f"Bienvenido al sistema Monitor, Tu cuenta se ha creado exitosamente, su nombre de usuario es: {user.username} y su email es: {user.email}",
            from_email="monitor.pruebas2000@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        from api.chirpstack_api import sync_user_to_chirpstack 
        sync_user_to_chirpstack(sender=User, instance=user, created=True, password_plaintext=password)
        return user
    
    def update(self, instance, validated_data):
        password = None
        if 'password' in validated_data:
            password = validated_data.get('password')
            instance.set_password(password)
            validated_data.pop('password')

        tenant = validated_data.pop('tenant', None)
        if tenant:
            instance.tenant = tenant

        user = super().update(instance, validated_data)
        instance.save()

        from api.chirpstack_api import sync_user_to_chirpstack 
        sync_user_to_chirpstack(sender=User, instance=user, created=False, password_plaintext=password)

        return user