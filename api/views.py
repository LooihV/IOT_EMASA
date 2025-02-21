#from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ProgrammerSerializer
from .models import Programador

# Create your views here.
class ProgrammerViewSet(viewsets.ModelViewSet):
    queryset = Programador.objects.all()
    serializer_class = ProgrammerSerializer
