import re
import requests
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
#from django.contrib.auth.models import User  # Usa tu modelo si es personalizado
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

CHIRPSTACK_API_URL = "http://chirpstack-rest-api:8090/api/users"
HEADERS = {
    "Authorization": f"Bearer {settings.CHIRPSTACK_JWT_TOKEN}",
    "Content-Type": "application/json"
}

def is_valid_email(email):
    """Valida si un string es un correo electrónico válido."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))



def get_chirpstack_user_id(email):
    """Busca el ID de un usuario en ChirpStack por su email."""
    try:
        # Incluye el parámetro 'limit' para la paginación
        params = {"limit": 50}
        response = requests.get(CHIRPSTACK_API_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        
        # Obtén la lista de usuarios
        users = response.json().get("result", [])
        
        # Recorre los usuarios para buscar el que coincida con el email
        for user in users:
            if user["email"].strip().lower() == email.strip().lower():
                return user["id"]
        
        # Si no se encuentra, imprime un mensaje y devuelve None
        print(f"No se encontró usuario con email {email} en ChirpStack.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error buscando usuario en ChirpStack: {e}")
    
    return None

@receiver(post_save, sender=User)
def sync_user_to_chirpstack(sender, instance, created, **kwargs):
    print(" Signal POST SAVE ejecutado para usuario Django")
    email = instance.email.strip().lower()

    if not is_valid_email(email):
        print(" Email inválido. No se sincroniza con ChirpStack.")
        return

    user_data = {
        "user": {
            "email": email,
            "note": f"Sincronizado desde Django para {instance.username}",
            "isAdmin": instance.is_superuser,
            "isActive":True,
            "password": instance.password #if created else "dummy"  # sólo al crear
        }
    }

    try:
        user_id = get_chirpstack_user_id(email)

        if created or not user_id:
            print("Usuario nuevo. Creando en ChirpStack...")
            response = requests.post(CHIRPSTACK_API_URL, headers=HEADERS, json=user_data)
        else:
            print(" Usuario ya existe. Actualizando en ChirpStack...")
            update_url = f"{CHIRPSTACK_API_URL}/{user_id}"
            user_data["user"].pop("password", None)  # No actualices contraseña
            response = requests.put(update_url, headers=HEADERS, json=user_data)

        print(f"STATUS: {response.status_code} | RESPUESTA: {response.text}")
        response.raise_for_status()

    except Exception as e:
        print(f" Error al sincronizar usuario con ChirpStack: {e}")

@receiver(pre_delete, sender=User)
def delete_user_from_chirpstack(sender, instance, **kwargs):
    print("🗑️ Signal PRE DELETE ejecutado para usuario Django")
    email = instance.email.strip().lower()

    if not is_valid_email(email):
        print("Email inválido. No se elimina de ChirpStack.")
        return

    try:
        # user_id de ChirpStack usando el email del usuario
        user_id = get_chirpstack_user_id(email)
        
        if user_id:
            # URL de eliminación usando el user_id
            delete_url = f"http://chirpstack-rest-api:8090/api/users/{user_id}"
            print(f"Eliminando usuario de ChirpStack con ID: {user_id}")

            # solicitud DELETE a ChirpStack
            response = requests.delete(delete_url, headers=HEADERS)
            response.raise_for_status()

            # Si es exitosa, imprime un mensaje
            print(f"Usuario eliminado de ChirpStack: {email} con ID: {user_id}")
        else:
            print(f"No se encontró usuario en ChirpStack con email: {email}")
    
    except requests.exceptions.RequestException as e:
        # Manejo de excepciones en caso de error en la solicitud a ChirpStack
        print(f"Error al eliminar usuario en ChirpStack: {e}")