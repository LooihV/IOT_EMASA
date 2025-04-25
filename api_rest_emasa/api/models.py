from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# models here.
# class Programador se puede cambiar en un futuro por la de Sensor 
# y cambiar los datos de esa clase por: Current, Preasure, Temperature, Voltage.
class Programador (models.Model):
    id = models.AutoField(primary_key=True)
    Usuario = models.CharField(max_length=100)
    Clave = models.CharField(max_length=50)
    Email = models.EmailField(unique=True, null=True)






class Tenant (models.Model):
    name = models.CharField(max_length=100, unique=True)
    chirpstack_id = models.CharField(max_length=36,blank=True, null=True)
    Can_have_gateways = models.BooleanField(default=False)
    private_gateways_up = models.BooleanField(default=False)
    private_gateways_down = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    
    email = models.EmailField(unique = True)
    #chirpstack_id = models.CharField(max_length=36,blank=True, null=True)
    
    ROLE_CHOISES = [
        ("viewer", "solo visualizacion"),
        ("controller", "controlar la maquina"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOISES, default="viewer")
    #groups = models.ManyToManyField("auth.Group", related_name ="custom_users",blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users_permissions",
        blank=True
    )


class CentralSystem (models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if CentralSystem.objects.exists() and not self.pk:
            raise ValueError("Solo puede existir una central.")
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name


class Machine (models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="machines")#DUEÑO DE LA MAQUINA
    central = models.ForeignKey(CentralSystem, on_delete=models.CASCADE)
    is_on = models.BooleanField(default=False)
    predictivo = models.BooleanField(default=False)
    gps = models.JSONField(default=dict)

    def __str__(self):
        return self.name



class Registro(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    Fecha = models.DateField(auto_now_add=True)
    TimeStamp = models.DateTimeField(auto_now_add=True)
    Pressure = models.FloatField(default=0.0)
    Current = models.FloatField(default=0.0)
    Temperature = models.FloatField(default=0.0)
    Voltage = models.FloatField(default=0.0)

    def __str__(self):
        return f"Registro de {self.machine.name if self.machine else 'Sin máquina'} - {self.Fecha}"