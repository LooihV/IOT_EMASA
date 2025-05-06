import random, os, string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializer import UserSerializer,TenantSerializer
from .models import  CustomUser,  Registro, Tenant #,User
from .models import Machine,CentralSystem
from .serializer import MachineSerializer, RegistroSerializer
from django.contrib.auth import authenticate
from .models import CustomToken
from django.utils.timezone import now
#from .chirpstack_api import ChirpstackApiClient
from .chirpstack_client import ChirpstackApiClient
from django.conf import settings


#from api_rest_emasa.api.chirpstack_api import create_user_in_chirpstack


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer





# Vista para generar token de autenticación
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

#---------------------


class CustomObtainAuthToken(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = CustomToken.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'created': token.created,
                'is_new': created
            })
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)



class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Machine.objects.all()
        return Machine.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        central = CentralSystem.objects.first()
        if not central:
            return Response({"error": "No hay una central registrada"},status=400)
        serializer.save(central=central, user=self.request.user)




    @action(detail=True, methods=['POST'])
    def toogle_power(self,request, pk=None):
        machine = self.get_object()
        if request.user.role != "controller":
            return Response({"Error, no tiene los permisos necesarios para realizar esta accion"},status=403)
        machine.is_on = not machine.is_on
        machine.save()
        return Response({"message": f"Màquina {machine.name} {'encendida' if machine.is_on else 'apagada'}"})
        


class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user   
        if user.is_superuser:
            return Registro.objects.all()
        return Registro.objects.filter(machine__user = user)


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    
    
    
       
    
    
class PasswordResetRequestViewSet(APIView):
    permission_classes = [IsAuthenticated]  #Sólo usuarios autenticados cambian sus cuentas asociadas.

    def post(self, request):
        email = request.data.get("email")

        # Verifica si el usuario existe y
        # Verifica que el usuario autenticado coincide con el correo
        if request.user.email != email:
            return Response({"error": "No puedes solicitar un cambio de contraseña para otro usuario."}, status=status.HTTP_403_FORBIDDEN)

        # Genera contraseña temporal
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        request.user.set_password(temp_password)  # Se asigna la nueva contraseña
        request.user.save()

        # Envia contraseña temporal por correo
        send_mail(
            "MONITOR: Recuperación de contraseña",
            f"Tu nueva contraseña temporal es: {temp_password}\n\nPor favor, cámbiala antes del próximo inicio de sesión.",
            "mario.bernalc@gmail.com",  # email configurado en settings.py
            [email],
            fail_silently=False,
        )

        return Response({"mensage": "Se ha enviado una contraseña temporal a tu correo."}, status=status.HTTP_200_OK)
    
class ChangePasswordViewSet(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        # Verifica si la contraseña actual es correcta
        if not user.check_password(old_password):
            return Response({"error": "La contraseña temporal-actual es incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar contraseña
        user.set_password(new_password)
        user.save()

        # Invalidar token anterior 
        Token.objects.filter(user=user).delete()

        return Response({"message": "Contraseña actualizada correctamente"}, status=status.HTTP_200_OK)


# ---------------- VIEWS DEL CONSUMO DE CHIRPSTACK GATEWAYS, DEVICES, APPLICATIONS ----------------


CHIRPSTACK_API_BASE = "http://chirpstack-rest-api:8090"
CHIRPSTACK_TOKEN = settings.CHIRPSTACK_JWT_TOKEN


class ChirpstackGatewayViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.register_gateway(request.data)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def get(self, request):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)

        try:
            if request.user.is_superuser:
                result = client.list_gateway()
            else:
                tenant = request.user.tenant
                if not tenant or not tenant.chirpstack_id:
                    return Response({"error": "El usuario no tiene un tenant válido asociado."}, status=403)
                
                tenant_id = tenant.chirpstack_id
                result = client.list_gateway(tenant_id=tenant_id)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
        
        
class ChirpstackGatewayDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    
    def delete(self, request, gateway_id):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)

        try:
            result = client.delete_gateway(gateway_id)
            return Response({"message": "Gateway eliminado correctamente"}, status=204)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        


class ChirpstackDeviceProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.create_device_profile(request.data)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ChirpstackDeviceViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.create_device(request.data)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class  ChirpstackDeviceDelGetView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, dev_eui):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.get_device(dev_eui)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


    def delete(self, request, dev_eui):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.delete_device(dev_eui)
            return Response({"message":"Device eliminado correctamente"},status=204)
        except Exception as e:
            return Response({"error":str(e)},status=400)
            
    
    
class ChirpstackDeviceActivationViewSet(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, dev_eui):
        
        
       """   ESTO SI SE VA A GENERAR LOS TOKENS DE APP_S_KEY Y NWK_S_KEY AUTOMATICAMENTE Y AL AZAR
            def generate_key():
            return os.urandom(16).hex()

        activation_data = {
            "dev_addr": "01020304",
            "app_s_key": generate_key(),
            "nwk_s_key": generate_key(),
            "f_cnt_up": 0,
            "f_cnt_down": 0
        }

        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.activate_device(dev_eui, activation_data)
            return Response({
                "message": "Dispositivo activado correctamente",
                "activation_data": activation_data,
                "result": result
            }, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)"""
        
        
       client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
       try:
            result = client.activate_device(dev_eui, request.data)
            return Response(result, status=status.HTTP_200_OK)
       except Exception as e:
            return Response({"error": str(e)}, status=400)
        
        

    def get(self, request, dev_eui):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.get_device_activation(dev_eui)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
        
class ChirpstackApplicationViewSet(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        user = request.user
        tenant = user.tenant

        if not tenant or not tenant.chirpstack_id:
            return Response({"error": "Usuario no tiene tenant asignado."}, status=403)

        application_data = request.data.copy()
        application_data["tenant_id"] = tenant.chirpstack_id  

        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.create_application(application_data)
            return Response(result, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
    def get(self, request):
     user = request.user
     tenant = user.tenant

     if not tenant or not tenant.chirpstack_id:
        return Response({"error": "Usuario no tiene tenant asignado."}, status=403)

     tenant_id = tenant.chirpstack_id
     limit = request.query_params.get("limit", 10)
     offset = request.query_params.get("offset", 0)
     search = request.query_params.get("search", "")

     client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
     try:
        result = client.list_application(tenant_id, limit, offset, search)
        return Response(result, status=200)
     except Exception as e:
        return Response({"error": str(e)}, status=400)
        

class ChirpstackApplicationDeleteView(APIView):
    permission_classes = [IsAuthenticated]


    def delete(self, request, application_id):
     client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
     try:
        result = client.delete_application(application_id)
        return Response({"message": "Aplicación eliminada correctamente"}, status=204)
     except Exception as e:
        return Response({"error": str(e)}, status=400)


class ChirpstackMQTTCertificateViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, application_id):
        client = ChirpstackApiClient(CHIRPSTACK_API_BASE, CHIRPSTACK_TOKEN)
        try:
            result = client.create_mqqt_certificate(application_id)
            return Response(result, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)