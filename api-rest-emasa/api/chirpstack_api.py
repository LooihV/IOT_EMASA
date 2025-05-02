import re
import requests
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
#from django.contrib.auth.models import User  # Usa tu modelo si es personalizado
from django.contrib.auth import get_user_model
from .models import Tenant, CustomUser, Machine #,User
from rest_framework.authtoken.models import Token
import binascii
import os

#User = get_user_model()
CustomUser = get_user_model()



#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
 #   if created:
  #      Token.objects.create(user=instance)

CHIRPSTACK_API_URL = "http://chirpstack-rest-api:8090/api/users"
CHIRPSTACK_TENANT_URL = "http://chirpstack-rest-api:8090/api/tenants"
CHIRPSTACK_GATEWAYS_URL = "http://chirpstack-rest-api:8090/api/gateways"
CHIRPSTACK_DEVICE_PROFILE_URL = "http://chirpstack-rest-api:8090/api/device-profiles"
CHIRPSTACK_DEVICES_URL = "http://chirpstack-rest-api:8090/api/devices"

HEADERS = {
    "Authorization": f"Bearer {settings.CHIRPSTACK_JWT_TOKEN}",
    "Content-Type": "application/json"
}

def is_valid_email(email):
    """Valida si un string es un correo electrónico válido."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


# -------------------- USERS POST, DELETE, CON Y SIN TENANT --------------------


def get_chirpstack_user_id(email):
    """Busca el ID de un usuario en ChirpStack por su email."""
    try:
        # Incluir el parámetro 'limit' ya que así funciona en el header de la solicitud para eliminar
        params = {"limit": 50}
        response = requests.get(CHIRPSTACK_API_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        
        # La lista de usuarios
        users = response.json().get("result", [])
        
        # Recorre los usuarios para buscar el que coincida con el email
        for user in users:
            if user["email"] == email:
                return user["id"]
        
        # Si no se encuentra, imprime un mensaje y devuelve None
        print(f"No se encontró usuario con email {email} en ChirpStack.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error buscando usuario en ChirpStack: {e}")
    
    return None

#@receiver(post_save, sender=CustomUser)
def sync_user_to_chirpstack(sender, instance, created, password_plaintext=None, **kwargs):
    print("Signal POST SAVE ejecutado para usuario Django")
    email = instance.email.strip()

    if not is_valid_email(email):
        print("Email inválido. No se sincroniza con ChirpStack.")
        return

    # Buscar el chirpstack_id del tenant si existe uno en el usuario
    tenant_payload = []
    if instance.tenant:
        tenant_name = instance.tenant.name
        tenant_id = instance.tenant.chirpstack_id or get_chirpstack_tenant_id_by_name(tenant_name)

        if tenant_id:
            tenant_payload.append({
                "tenantId": tenant_id,
                "isAdmin": True,
                "isDeviceAdmin": True,
                "isGatewayAdmin": True
            })
        else:
            print(f"Tenant '{tenant_name}' no encontrado en ChirpStack. No se asociará el usuario.")

    user_data = {
        "user": {
            "email": email,
            "note": f"Sincronizado desde Django para {instance.username}",
            "isAdmin": instance.is_superuser,
            "isActive": True,
        },
        "tenants": tenant_payload
    }

    try:
        user_id = get_chirpstack_user_id(email)

        if created:
            print("Usuario NUEVO. Creando en ChirpStack...")
            if password_plaintext:
                user_data["password"] = password_plaintext
            response = requests.post(CHIRPSTACK_API_URL, headers=HEADERS, json=user_data)
            print(f"STATUS CREACIÓN: {response.status_code} | RESPUESTA: {response.text}")
            response.raise_for_status()

        else:
            if not user_id:
                print(f"Error crítico: No se encontró user_id en ChirpStack para {email}. No se puede actualizar.")
                return

            print("Usuario EXISTENTE. Actualizando en ChirpStack...")
            update_url = f"{CHIRPSTACK_API_URL}/{user_id}"

            # Primero actualiza los datos generales
            response = requests.put(update_url, headers=HEADERS, json=user_data)
            print(f"STATUS ACTUALIZACIÓN: {response.status_code} | RESPUESTA: {response.text}")
            response.raise_for_status()

            # Luego actualiza el password si es necesario
            if password_plaintext:
                print("Actualizando contraseña en ChirpStack...")
                password_url = f"{CHIRPSTACK_API_URL}/{user_id}/password"
                password_payload = {"password": password_plaintext}
                password_response = requests.post(password_url, headers=HEADERS, json=password_payload)
                print(f"STATUS CONTRASEÑA: {password_response.status_code} | RESPUESTA: {password_response.text}")
                password_response.raise_for_status()

    except Exception as e:
        print(f"Error al sincronizar usuario con ChirpStack: {e}")

@receiver(pre_delete, sender=CustomUser)
def delete_user_from_chirpstack(sender, instance, **kwargs):
    print(" Signal PRE DELETE ejecutado para usuario Django")
    email = instance.email.strip().lower()

    if not is_valid_email(email):
        print("Email inválido. No se elimina de ChirpStack.")
        return

    try:
        # user_id de ChirpStack según a el email del usuario
        user_id = get_chirpstack_user_id(email)
        
        if user_id:
            # URL de eliminación usando el user_id
            delete_url = f"http://chirpstack-rest-api:8090/api/users/{user_id}"
            print(f"Eliminando usuario de ChirpStack con ID: {user_id}")

            # solicitud DELETE a ChirpStack
            response = requests.delete(delete_url, headers=HEADERS)
            response.raise_for_status()

            # Si todo sale bien
            print(f"Usuario eliminado de ChirpStack: {email} con ID: {user_id}")
        else:
            print(f"No se encontró usuario en ChirpStack con email: {email}")
    
    except requests.exceptions.RequestException as e:
        # Manejo de excepciones en caso de error en la solicitud a ChirpStack
        print(f"Error al eliminar usuario en ChirpStack: {e}")
        
        

#  ------------------------- TENANTS POST Y DELETE -------------------------

@receiver(post_save, sender=Tenant)
def sync_tenant_to_chirpstack(sender, instance, created, **kwargs):
    if created and not instance.chirpstack_id:
        print("Creando Tenant en ChirpStack...")

        tenant_data = {
            "tenant": {
                "canHaveGateways": True,
                "description": "Desde django",
                "maxDeviceCount": 0,
                "maxGatewayCount": 0,
                "name": instance.name,
                "privateGatewaysDown": False,
                "privateGatewaysUp": False,
                "tags": {}
            }
        }

        try:
            response = requests.post(
                CHIRPSTACK_TENANT_URL,
                headers=HEADERS,
                json=tenant_data
            )
            response.raise_for_status()
            chirpstack_id = response.json()["id"]

            print(f"Tenant creado en ChirpStack con ID: {chirpstack_id}")

            # Guardar ID en Django
            instance.chirpstack_id = chirpstack_id
            instance.save(update_fields=["chirpstack_id"])

        except requests.exceptions.RequestException as e:
            print(f"Error al crear tenant en ChirpStack: {e}")
            


def get_chirpstack_tenant_id_by_name(name):
    """Obtiene el ID del tenant en ChirpStack dado su nombre."""
    try:
        params = {"limit": 50}
        response = requests.get(CHIRPSTACK_TENANT_URL, headers=HEADERS, params=params)
        response.raise_for_status()

        tenants = response.json().get("result", [])
        for tenant in tenants:
            if tenant["name"] == name:
                return tenant["id"]
        
        print(f"No se encontró tenant con nombre: {name}")

    except requests.exceptions.RequestException as e:
        print(f"Error al buscar tenant en ChirpStack: {e}")
    
    return None
##
@receiver(pre_delete, sender=Tenant)
def delete_tenant_from_chirpstack(sender, instance, **kwargs):
    print("Signal PRE DELETE ejecutado para Tenant Django")
    name = instance.name.strip()

    try:
        tenant_id = instance.chirpstack_id or get_chirpstack_tenant_id_by_name(name)

        if tenant_id:
            delete_url = f"{CHIRPSTACK_TENANT_URL}/{tenant_id}"
            print(f"Eliminando tenant de ChirpStack con ID: {tenant_id}")

            response = requests.delete(delete_url, headers=HEADERS)
            response.raise_for_status()

            print(f"Tenant eliminado de ChirpStack: {name} con ID: {tenant_id}")
        else:
            print(f"No se encontró tenant en ChirpStack con nombre: {name}")

    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar tenant en ChirpStack: {e}")
        
        
        
# --------------------- GATEWAY ---------------------

def sync_gateway_to_chirpstack(gateway_id, name, tenant_name, description="Desde Django", stats_interval=30):
    tenant_id = get_chirpstack_tenant_id_by_name(tenant_name)
    if not tenant_id:
        print(f"Tenant '{tenant_name}' no encontrado. No se puede crear Gateway.")
        return

    payload = {
        "gateway": {
            "gatewayId": gateway_id,
            "name": name,
            "description": description,
            "statsInterval": stats_interval,
            "tenantId": tenant_id
        }
    }

    try:
        response = requests.post(CHIRPSTACK_GATEWAYS_URL, headers=HEADERS, json=payload)
        print(f"[Gateway] STATUS {response.status_code} | RESPUESTA: {response.text}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error creando gateway: {e}")


# --------------------- DEVICE PROFILE ---------------------

def sync_device_profile_to_chirpstack(name, tenant_name, region="US915"):
    tenant_id = get_chirpstack_tenant_id_by_name(tenant_name)
    if not tenant_id:
        print(f"Tenant '{tenant_name}' no encontrado. No se puede crear perfil.")
        return

    payload = {
        "deviceProfile": {
            "name": name,
            "region": region,
            "macVersion": "LORAWAN_1_0_3",
            "regParamRevision": "RP002_1_0_1",
            "supportsOtaa": False,
            "abpRx1Delay": 0,
            "abpRx1DrOffset": 0,
            "abpRx2Dr": 0,
            "abpRx2Freq": 0,
            "supportsClassB": False,
            "supportsClassC": False,
            "payloadCodecRuntime": "NONE",
            "isRlay": False,
            "isRlayEd": False,
            "tenantId": tenant_id
        }
    }

    try:
        response = requests.post(CHIRPSTACK_DEVICE_PROFILE_URL, headers=HEADERS, json=payload)
        print(f"[DeviceProfile] STATUS {response.status_code} | RESPUESTA: {response.text}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error creando device profile: {e}")


# --------------------- DEVICE ---------------------

def sync_device_to_chirpstack(dev_eui, name, description, profile_id, application_id):
    payload = {
        "device": {
            "name": name,
            "description": description,
            "devEui": dev_eui,
            "deviceProfileId": profile_id,
            "isDisabled": False,
            "applicationId": application_id
        }
    }

    try:
        response = requests.post(CHIRPSTACK_DEVICES_URL, headers=HEADERS, json=payload)
        print(f"[Device] STATUS {response.status_code} | RESPUESTA: {response.text}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error creando device: {e}")
        
@receiver(post_save, sender=Machine)
def sync_machine_as_device(sender, instance, created, **kwargs):
    if not created:
        return

    print("Sincronizando Machine como device en ChirpStack...")

    user = instance.user
    tenant = user.tenant

    if not tenant or not tenant.chirpstack_id:
        print("La máquina no tiene un tenant válido, no se puede sincronizar.")
        return

    # Crear device profile si no existe
    device_profile_name = f"profile-{tenant.name}"
    sync_device_profile_to_chirpstack(device_profile_name, tenant.name)

    # Buscar ID del perfil recién creado
    try:
        response = requests.get(CHIRPSTACK_DEVICE_PROFILE_URL, headers=HEADERS, params={"limit": 100})
        response.raise_for_status()
        profiles = response.json().get("result", [])
        profile_id = next((p["id"] for p in profiles if p["name"] == device_profile_name), None)
    except Exception as e:
        print("Error obteniendo device profiles:", e)
        return

    if not profile_id:
        print(f"No se encontró el profile '{device_profile_name}' después de crearlo.")
        return

    # Crear una aplicación si es necesario
    application_id = tenant.chirpstack_id  # Opcionalmente crea/usa una aplicación por tenant

    # dev_eui ficticio único (cambiar despues por los #de serie de cada device 16 caracteres)
    dev_eui = binascii.hexlify(os.urandom(8)).decode()

    sync_device_to_chirpstack(
        dev_eui=dev_eui,
        name=instance.name,
        description="Dispositivo creado desde Django",
        profile_id=profile_id,
        application_id=application_id
    )