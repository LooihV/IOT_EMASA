import requests

CHIRPSTACK_API_URL = "http://lorawan_server-chirpstack-rest-api-1:8090/api/users"
CHIRPSTACK_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjQ1YzE1NzAxLTk4ZjEtNGQ5My04OTk0LTEzOGFmZjVmMjhkZCIsInR5cCI6ImtleSJ9.GkOcWf0y_UtlIuRi41nefb3hNzEDBWXeyX3BsBht-5A"
TENANT_ID = "5e0b31d5-0edd-4327-9dde-d4e009b69c6e"

HEADERS = {
    "Content-Type": "application/json",
    "Grpc-Metadata-Authorization": CHIRPSTACK_TOKEN
}

def create_user_in_chirpstack(email, password, is_superuser):
    user_data = {
        "password": password,
        "user": {
            "email": email,
            "isActive": True,
            "isAdmin": is_superuser,
            "note": "Usuario creado desde Django"
        }
    }

    if not is_superuser:
        user_data["tenants"] = [
            {
                "tenantId": TENANT_ID,
                "isAdmin": True,
                "isDeviceAdmin": True,
                "isGatewayAdmin": True
            }
        ]

    response = requests.post(CHIRPSTACK_API_URL, json=user_data, headers=HEADERS)

    try:
        return response.status_code, response.json()
    except Exception as e:
        return response.status_code, {"error": str(e)}

def update_user_in_chirpstack(user_id, new_email, is_active):
    update_data = {
        "user": {
            "email": new_email,
            "isActive": is_active,
            "note": "Actualizado desde Django"
        }
    }

    url = f"{CHIRPSTACK_API_URL}/{user_id}"
    response = requests.put(url, json=update_data, headers=HEADERS)

    try:
        return response.status_code, response.json()
    except Exception as e:
        return response.status_code, {"error": str(e)}

def delete_user_in_chirpstack(user_id):
    url = f"{CHIRPSTACK_API_URL}/{user_id}"
    response = requests.delete(url, headers=HEADERS)

    return response.status_code