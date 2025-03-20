#from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializer import ProgrammerSerializer,UserSerializer
from .models import Programador, CustomUser, User, Registro
from .models import Machine,CentralSystem
from .serializer import MachineSerializer, RegistroSerializer



class ProgrammerViewSet(viewsets.ModelViewSet):
    queryset = Programador.objects.all()
    serializer_class = ProgrammerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Programador.objects.all()
        return Programador.objects.filter(Usuario=user.username)

    def get_permissions(self):
        """Restringir acceso según el tipo de usuario."""
        if self.request.user.is_superuser:
            return [IsAuthenticated()]  # Acceso total para admin
        return [IsAuthenticated()]  # Acceso solo a datos del usuario


# Vista para generar token de autenticación
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    





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
        return Registro.objects.filter(maquina__user = user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]