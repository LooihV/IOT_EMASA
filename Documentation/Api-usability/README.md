# DOCUMENTACIÓN GITHUB

## Resultados y estructura de los endpoints de la api-rest

#### Autenticación

POST /api/v1/token/

Obtiene un token de autenticación personalizado.

##### Request:

	{
	 "username": "usuario",
 	 "password": "contraseña"
	}

##### Response:

	{
 	"token": "<token>"
	}

#### Genera Nueva Contraseña temporal

POST /api/v1/pass/reset/

Genera una contraseña temporal para el usuario autenticado y la envía por correo.

##### Request: (tiene que estar autenticado)

	{
 	 "email": "usuario@dominio.com"
	}

##### Response:

	{
 	 "mensage": "Se ha enviado una contraseña temporal a tu correo."
	}

#### Cambio de contraseña temporal por una nueva definida.

POST /api/v1/pass/change/

Cambia la contraseña del usuario por una nueva.

##### Request: (autenticado)

	{
 	 "old_password": "temporalRecibida",
 	 "new_password": "contraseñaNueva"
	}

##### Response:

	{
 	 "message": "Contraseña actualizada correctamente en ambas APIs"
	}

#### Administrar usuarios.

GET /api/v1/Users/

Lista usuarios. Solo los superusers pueden ver actuar sobre todos los usuarios.

POST /api/v1/Users/

Crea un usuario nuevo.

##### Request: (autenticado)

![Image](https://github.com/user-attachments/assets/9f82f4cf-4feb-4523-822f-8a6f4a2f1483)

##### Response:

	{
  	 "message": “Usuario creado con éxito"
	}

DELETE /api/v1/Users/id del usuario

##### Response:

	 Elimina un usuario.

#### Maquinas (Devices)

GET /api/v1/Maquinas/

Lista las máquinas del usuario autenticado. Si es superuser, ve todas.

POST /api/v1/Maquinas/

Crea una nueva máquina asociada al usuario y la central activa.

##### Request: (autenticado)

![Image](https://github.com/user-attachments/assets/7ce3f387-ac42-4a6a-b848-62b6f79ec775)

##### Response:

	{
  	 "message": "Máquina encendida"
	}

#### Registros

GET /api/v1/Registro/

Lista registros de las máquinas del usuario. Si es superuser, ve todos.

POST /api/v1/ Registro/

Crea un nuevo registro asociado a una máquina y a un usuario.

##### Request: (autenticado)

![Image](https://github.com/user-attachments/assets/7bf5d403-a379-4113-a56b-4620ffa9bee1)

##### Response:

	{
 	 El nuevo registro creado.
	}

## ChirpStack API Proxy (consumo desde Django)

La API EMASA actúa como cliente hacia ChirpStack, realizando operaciones de forma transparente. Las rutas siguientes proxyfian las llamadas REST a ChirpStack utilizando el JWT Token configurado en entorno:

Sincronización bidireccional con ChirpStack (users y tenants)

El archivo chirpstack\_api.py contiene la lógica que permite mantener sincronizados los usuarios y tenants entre EMASA y ChirpStack:

- Creación de usuarios: Cuando se crea un usuario en EMASA (vía señales post\_save), también se crea en ChirpStack con mismo email y rol.
- Eliminación de usuarios: Se elimina automáticamente también en ChirpStack (pre\_delete).
- Asignación de tenants: Si el usuario en EMASA tiene un tenant relacionado, se sincroniza y asocia también en ChirpStack.
- Cambio de contraseña: Al cambiar contraseña en EMASA (temporal o nueva), se actualiza también en ChirpStack mediante peticiones a /api/users/{id}/password.
- Creación de tenants: Tenants creados en EMASA pueden sincronizar su chirpstack\_id con la plataforma ChirpStack.

Toda esta lógica se implementa mediante funciones auxiliares get\_chirpstack\_user\_id, sync\_user\_to\_chirpstack, update\_chirpstack\_user\_password y llamadas HTTP con requests.


#### Applications

GET /api/v1/chirpstack/applications/ - Lista las aplicaciones del tenant del usuario.

##### Response:
	{

 	"totalCount": 1,
 	 "result": [
		{
	          "id": "3231a7fa-61e6-4ed3-854c-6aa0bc3c40a6",
	          "createdAt": "2025-05-13T16:12:12.859046Z",
	          "updatedAt": "2025-05-13T16:12:12.859046Z",
	          "name": "appi01",
	          "description": "drf"
		}
					]
	}

POST /api/v1/chirpstack/applications/ - Crea una aplicación asociada al tenant.

##### Request: (autenticado)

	{
	 "name": "normalito",
	 "description": "una descripción"
	}

##### Response: (autenticado)

	{
 	 El registro de las applications creadas
	}

DELETE /api/v1/chirpstack/applications/{id}/ - Elimina una aplicación.

#### Gateways

GET /api/v1/chirpstack/gateways/ - Lista todos los gateways o solo los del tenant asociado al usuario.

##### Response: (autenticado)

	{
	"totalCount": 1,
	 "result": [
	   {
		 "tenantId": "216382fe-dd3d-4e0e-9945-202c4400546b",
		 "gatewayId": "a84041fdfe2764b6",
		 "name": "test-gateway",
		 "description": "test",
		 "location": {
		 "latitude": 0,
		 "longitude": 0,
		 "altitude": 0,
		 "source": "UNKNOWN",
		 "accuracy": 0
				},
		 "properties": {},
		 "createdAt": "2025-05-13T16:14:37.092479Z",
		 "updatedAt": "2025-05-13T16:14:37.092479Z",
		 "lastSeenAt": null,
		 "state": "NEVER\_SEEN"
	   }
			 ]
	}

POST /api/v1/chirpstack/gateways/ - Registra un nuevo gateway.

##### Request: (Autenticado)

	{
	 "gatewayId": "a84041fdfe2764b6",
	 "name": "test-gateway",
	 "description": "test",
	 "statsInterval": 30,
	 "tenantId": "tu-uuid-de-tenant"
	}

##### Response: (autenticado)

	{
	 El registro de los Gateways creados
	}

DELETE /api/v1/chirpstack/gateways/{id}/ - Elimina un gateway por su ID.

#### Device Profiles

POST /api/v1/chirpstack/device-profiles/ - Crea un perfil de dispositivo.

MQTT Certificate

##### Request: (Autenticado)

	{
	 "name": "perfil\_sensor\_temp",
	 "region": "EU868",
	 "mac\_version": "1.0.2",
	 "reg\_params\_revision": "B",
	 "supports\_join": true,
	 "rx\_delay\_1": 1,
	 "rx\_datarate\_2": 0,
	 "rx\_freq\_2": 869525000,
	 "factory\_preset\_freqs": [868100000, 868300000, 868500000],
	 "max\_eirp": 14,
	 "uplink\_interval": "60",
	 "supports\_class\_b": false,
	 "supports\_class\_c": false,
	 "tenant\_id": "un tenant\_id"
	}

##### Response: (autenticado)

	{
	 El registro del device profile creado.
	}

POST /api/v1/chirpstack/applications/{id}/mqtt-certificate/ - Genera certificado MQTT para una aplicación.

#### Devices

POST /api/v1/chirpstack/devices/ - Registra un nuevo dispositivo.

##### Request: (autenticado)

	{
	 "application\_id": "f6a6e800-bc8d-4a59-9006-0a69f7f9decb",
	 "description": "Sensor temperatura",
	 "dev\_eui": "70b3d57ed006e229",
	 "device\_profile\_id": "d73f8703-3541-4ed1-9993-8d5566f002b2",
	 "name": "sensor-temp-001",
	 "skip\_fcnt\_check": true,
	 "is\_disabled": false
	}

##### Response: (autenticado)

	{
	 Listado del device creado.
	}

GET /api/v1/chirpstack/devices/{dev\_eui}/ - Consulta un dispositivo por DevEUI.

##### Response: (autenticado)

	{
	 "device": {
	 "devEui": "0004a30b001c0530",
	 "name": "sensor-temp-001",
	 "description": "Sensor temperatura",
	 "applicationId": "56e87d7b-1458-43e2-b9a6-3a5c5b25c2d6",
	 "deviceProfileId": "efd23bbc-a295-4fd6-ac59-1ab7f417c02f",
	 "skipFcntCheck": true,
	 "isDisabled": false,
	 "variables": {},
	 "tags": {},
	 "joinEui": "0000000000000000"
		 },
	 "createdAt": "2025-05-08T19:44:47.868434Z",
	 "updatedAt": "2025-05-08T19:44:47.868434Z",
	 "lastSeenAt": null,
	 "deviceStatus": null,
	 "classEnabled": "CLASS\_A"
	}

DELETE /api/v1/chirpstack/devices/{dev\_eui}/ - Elimina un dispositivo.

##### Response: (autenticado)

	{
	 "message": "Device eliminado correctamente"
	}

#### Device Activation

POST /api/v1/chirpstack/devices/{dev\_eui}/activation/ - Activa un dispositivo (con claves nwk\_s\_key, app\_s\_key, etc.).

##### Request: (autenticado)

	{
	 "dev\_addr": "260CB229",
	 "app\_s\_key": "53C020841486263981FA77355D278762",
	 "nwk\_s\_key": "4978CB8E7FFBD46BC570FE11F17FA56E",
	 "f\_cnt\_up": 0,
	 "f\_cnt\_down": 0
	}

##### Response: (Autenticado)

	{
	 Status 200 ok
	}

## Test pruebas cómo se realizan las pruebas de la API.

Para realizar las pruebas de la api rest, se ejecutan una serie de comandos desde la terminal, dependiendo si se quieren ejecutar todos los test al mismo tiempo o sólo una función a la vez. Primero se debe asegurar de que su contenedor web de la api-rest-emasa esté corriendo, luego dentro de la ruta: ```json
IOT\_EMASA/api-rest-emasa/
``` se ejecutan los siguientes comandos:

**1. Si se quieren ejecutar todos los test a la vez:** docker-compose exec web Python manage.py test api.tests
**2. Para ejecutar el test del token:** docker-compose exec web Python manage.py test api.tests.test\_auth
**3. Para ejecutar el test de user:** docker-compose exec web Python manage.py test api.tests.test\_users
**4. Para ejecutar el test del tenant:** docker-compose exec web Python manage.py test api.tests.test\_tenants
**5. Para ejecutar el test de applications:** docker-compose exec web Python manage.py test api.tests.test\_applications
**6. Para ejecutar el test de gateways:** docker-compose exec web Python manage.py test api.tests.test\_gateways
**7. Para ejecutar el test de device profiles:** docker-compose exec web Python manage.py test api.tests.test\_device\_profiles
**8. Para ejecutar el test de devices:** docker-compose exec web Python manage.py test api.tests.test\_devices
**9. Para ejecutar el test de device activation:** docker-compose exec web Python manage.py test api.tests.test\_device\_activation
**10. Para ejecutar el test de password:** docker-compose exec web Python manage.py test api.tests.test\_password
**11. Para ejecutar el test de user sincronizacion con chirpstack:** docker-compose exec web Python manage.py test api.tests.test\_user\_sync
**12. Para ejecutar el test de tenant sincronización con chirpstack:** docker-compose exec web Python manage.py test api.tests.test\_tenant\_sync

La carpeta que contiene el código de lo tests se encuentra en la ruta: 
```json
IOT_EMASA/api-rest-emasa/api/tests
```

## Sincronización con la base de datos.

La sincronización con la base de datos se realiza por medio de variables de entorno que se comunican entre el código de la db en la ruta IOT\_EMASA/api-rest-emasa/drf/settings.py:

	DATABASES = {
		 'default': {
		 'ENGINE': 'django.db.backends.postgresql',
		 'NAME': os.environ.get('POSTGRES\_DB'), 
		 'USER': os.environ.get('POSTGRES\_USER'), 
		 'PASSWORD': os.environ.get('POSTGRES\_PASSWORD'), 
		 'HOST': os.environ.get('POSTGRESQL\_HOST'),
		 }
	}

Y un archivo .env.prod ubicado en la raíz del proyecto que contiene los datos de la base de datos cómo:

**POSTGRESQL\_HOST=** el hostname de la db, en caso de este proyecto es el nombre del contenedor de persistance

**POSTGRES\_USER=** El nombre de usuario de la base de datos

**POSTGRES\_PASSWORD=** La contraseña asociada a la base de datos

**POSTGRES\_DB=** El nombre de la base de datos

**POSTGRES\_PORT=** El puerto dónde corre la db

El settings de mi proyecto django ```
IOT\_EMASA/api-rest-emasa/drf/settings.py
``` se comunica con el .env.prod gracias a que el contenedor de la api ```
IOT\_EMASA/api-rest-emasa/docker-compose.prod.yml
``` lo tiene declarado. 

	Web:
 		 env_file:
 			  - path: ../.env.prod


## Respuestas y transacciones.

#### 1. Register Users

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 2. Register Machines

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 3. Boot Notification "Register"

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 4. Set Machines

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 5. SendData

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 6. Data Transfer Request

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 7. Diagnostic Status

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 8. Change Availability Request

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 9. Stop Transaction Response

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**


#### 10. Change Availability Response

  **- Descripción:**
     **- Módulo:**
	 **- Tipo:**
