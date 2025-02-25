from django.db import models

# Create your models here.
class Programador (models.Model):
    Usuario = models.CharField(max_length=100)
    Clave = models.CharField(max_length=50)
    Datos = models.PositiveIntegerField()
    Datos2 = models.DecimalField(max_digits=10,decimal_places=3)
