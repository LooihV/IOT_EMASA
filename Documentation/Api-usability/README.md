#  GITHUB API DOCUMENTATION

The classes and functions of the api are declared at models.py file, the serializer.py file is the file which can perform the classes actions and the views.py is the users view from the drf panel administration the routes are declared at the urls.py file and the actions related to chirpstack are detail at the second (2) subtitle of this file.

## Content

[1. Results and structure of api-rest endpoints](#1-Results-and-structure-of-api-rest-endpoints)

[1.1. Authentication](#11-Authentication)

[1.2. Generates New Temporary Password](#12-Generates-New-Temporary-Password)

[1.3. Change of temporary password for a new defined one.](#13-Change-of-temporary-password-for-a-new-defined-one)

[1.4. Manage users.](#14-Manage-users)

[1.5. Machines (Devices)](#15-Machines-Devices)

[1.6. Records](#16-Records)

[2. ChirpStack API Proxy (Django consumption)](#2-ChirpStack-API-Proxy-Django-consumption)

[2.1. Applications](#21-Applications)

[2.2. Gateways](#22-Gateways)

[2.3. Device Profiles](#23-Device-Profiles)

[2.4. Devices](#24-Devices)

[2.5. Device Activation](#25-Device-Activation)

[3. Tests of how API tests are performed.](#3-Tests-of-how-API-tests-are-performed)

[4. Database synchronization.](#4-Database-synchronization)

[5. Responses and transactions.](#5-Responses-and-transactions)

[5.1. Register Users](#51-Register-Users)

[5.2. Register Machines](#52-Register-Machines)

[5.3. Boot Notification (Register)](#53-Boot-Notification-Register)

[5.4. Set Machines](#54-Set-Machines)

[5.5. SendData](#55-SendData)

[5.6. Data Transfer Request](#56-Data-Transfer-Request)

[5.7. Diagnostic Status](#57-Diagnostic-Status)

[5.8. Change Availability Request](#58-Change-Availability-Request)

[5.9. Stop Transaction Response](#59-Stop-Transaction-Response)

[5.11. Change Availability Response](#511-Change-Availability-Response)






## 1. Results and structure of api-rest endpoints

#### 1.1. Authentication

POST /api/v1/token/

Obtains a personalized authentication token.

##### Request:

	{
	 "username": "user",
 	 "password": "the password"
	}

##### Response:

	{
 	"token": "<token>"
	}

#### 1.2. Generates New Temporary Password

POST /api/v1/pass/reset/

Generates a temporary password for the authenticated user and sends it by mail.

##### Request: (Have to be authenticated)

	{
 	 "email": "user@domain.com"
	}

##### Response:

	{
 	 "mensage": "We have send a temporary password to your email."
	}

#### 1.3. Change of temporary password for a new defined one.

POST /api/v1/pass/change/

Change de users password for a new one.

##### Request: (Have to be authenticated)

	{
 	 "old_password": "temporarypassword",
 	 "new_password": "thenewpassword"
	}

##### Response:

	{
 	 "message": "Password correctly updated in both APIs"
	}

#### 1.4. Manage users.

GET /api/v1/Users/

Users list. Just superusers can see and act over all the users.

POST /api/v1/Users/

Creates a new user.

##### Request: (Have to be authenticated)

![Image](https://github.com/user-attachments/assets/9f82f4cf-4feb-4523-822f-8a6f4a2f1483)

##### Response:

	{
  	 "message": “User succesfully created"
	}

DELETE /api/v1/Users/user id

##### Response:

	 {
  	   "message": "deleted user"
      	 }

#### 1.5. Machines (Devices)

GET /api/v1/Maquinas/

List the machines from the authenticated user. If is superuser, see all.
POST /api/v1/Maquinas/

Creates a new machine asociated to the user and the active central.

##### Request: (Have to be authenticated)

![Image](https://github.com/user-attachments/assets/7ce3f387-ac42-4a6a-b848-62b6f79ec775)

##### Response:

	{
  	 "message": "Machine on"
	}

#### 1.6. Records

GET /api/v1/Registro/

Lists the records of the users machines. If is superuser, see all.

POST /api/v1/ Registro/

Creates a new register asociated to a machine and a user.

##### Request: (Have to be authenticated)

![Image](https://github.com/user-attachments/assets/7bf5d403-a379-4113-a56b-4620ffa9bee1)

##### Response:

	{
 	 The new record.
	}

## 2. ChirpStack API Proxy (Django consumption)

The EMASA API acts as a client to ChirpStack, transparently performing operations. The following routes proxy REST calls to ChirpStack using the JWT Token configured in the environment:

Bidirectional synchronization with ChirpStack (users and tenants)

The file chirpstack\_api.py contains the logic to keep users and tenants synchronized between EMASA and ChirpStack:

- User creation: When a user is created in EMASA (via post_save signals), it is also created in ChirpStack with the same email and role.
- User deletion: It is also automatically deleted in ChirpStack (pre-delete).
- Tenant assignment: If the user in EMASA has a related tenant, it is synchronized and associated also in ChirpStack.
- Password change: When changing password in EMASA (temporary or new), it is also updated in ChirpStack through requests to /api/v1/pass/reset/ if you forget your password and ask for a temporary and api/v1/pass/change/ if is a new one.
- Tenant creation: Tenants created in EMASA can synchronize their chirpstack_id with the ChirpStack platform.

All this logic is implemented by means of auxiliary functions get\_chirpstack\_user\_id, sync\_user\_to\_chirpstack, update\_chirpstack\_user\_password and HTTP calls using requests.


#### 2.1. Applications

GET /api/v1/chirpstack/applications/ - Lists the users tenants applications.

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

POST /api/v1/chirpstack/applications/ - Creates an application asociated to tenant.

##### Request: (Have to be authenticated)

	{
	 "name": "normal",
	 "description": "a description"
	}

##### Response: (Have to be authenticated)

	{
 	 El registro de las applications creadas
	}

DELETE /api/v1/chirpstack/applications/{id}/ - Deletes an application.

#### 2.2. Gateways

GET /api/v1/chirpstack/gateways/ - Lists all the gateways or only those of the tenant associated with the user.

##### Response: (Have to be authenticated)

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

POST /api/v1/chirpstack/gateways/ - Register a new gateway.

##### Request: (Have to be authenticated)

	{
	 "gatewayId": "a84041fdfe2764b6",
	 "name": "test-gateway",
	 "description": "test",
	 "statsInterval": 30,
	 "tenantId": "tu-uuid-de-tenant"
	}

##### Response: (Have to be authenticated)

	{
	 El registro de los Gateways creados
	}

DELETE /api/v1/chirpstack/gateways/{id}/ - Deletes a gateway by ID.

#### 2.3. Device Profiles

POST /api/v1/chirpstack/device-profiles/ - Creates a device profile.

MQTT Certificate

##### Request: (Have to be authenticated)

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

##### Response: (Have to be authenticated)

	{
	 The record of the device profile created.
	}

POST /api/v1/chirpstack/applications/{id}/mqtt-certificate/ - Generates a MQTT certificate for an application.

#### 2.4. Devices

POST /api/v1/chirpstack/devices/ - Register a new device.

##### Request: (Have to be authenticated)

	{
	 "application\_id": "f6a6e800-bc8d-4a59-9006-0a69f7f9decb",
	 "description": "Sensor temperatura",
	 "dev\_eui": "70b3d57ed006e229",
	 "device\_profile\_id": "d73f8703-3541-4ed1-9993-8d5566f002b2",
	 "name": "sensor-temp-001",
	 "skip\_fcnt\_check": true,
	 "is\_disabled": false
	}

##### Response: (Have to be authenticated)

	{
	 The record of the created device.
	}

GET /api/v1/chirpstack/devices/{dev\_eui}/ - Consult a device by DevEUI.

##### Response: (Have to be authenticated)

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

DELETE /api/v1/chirpstack/devices/{dev\_eui}/ - Deletes a device.

##### Response: (Have to be authenticated)

	{
	 "message": "Device successfully deleted"
	}

#### 2.5. Device Activation

POST /api/v1/chirpstack/devices/{dev\_eui}/activation/ - Activates a device (with keys nwk\_s\_key, app\_s\_key, etc.).

##### Request: (Have to be authenticated)

	{
	 "dev\_addr": "260CB229",
	 "app\_s\_key": "53C020841486263981FA77355D278762",
	 "nwk\_s\_key": "4978CB8E7FFBD46BC570FE11F17FA56E",
	 "f\_cnt\_up": 0,
	 "f\_cnt\_down": 0
	}

##### Response: (Have to be authenticated)

	{
	 Status 200 ok
	}

## 3. Tests of how API tests are performed.

To run the api rest tests, you run a series of commands from the terminal, depending on whether you want to run all the tests at the same time or just one function at a time. You must first make sure that your api-rest-emasa web container is running, then inside the path: 
IOT\_EMASA/api-rest-emasa/
 the following commands are executed:

**1. If you want to run all tests at the same time:** docker-compose exec web Python manage.py test api.tests

**2. To execute the token test:** docker-compose exec web Python manage.py test api.tests.test\_auth

**3. To execute the user test:** docker-compose exec web Python manage.py test api.tests.test\_users

**4. To execute the tenant test:** docker-compose exec web Python manage.py test api.tests.test\_tenants

**5. To execute the applications test:** docker-compose exec web Python manage.py test api.tests.test\_applications

**6. To execute the gateways test:** docker-compose exec web Python manage.py test api.tests.test\_gateways

**7. To execute the device profiles test:** docker-compose exec web Python manage.py test api.tests.test\_device\_profiles

**8. To execute the devices test:** docker-compose exec web Python manage.py test api.tests.test\_devices

**9. To execute the device activation test:** docker-compose exec web Python manage.py test api.tests.test\_device\_activation

**10. To execute the password test:** docker-compose exec web Python manage.py test api.tests.test\_password

**11. To execute the user sincronizacion con chirpstack test:** docker-compose exec web Python manage.py test api.tests.test\_user\_sync

**12. To execute the tenant sincronización con chirpstack test:** docker-compose exec web Python manage.py test api.tests.test\_tenant\_sync


The folder containing the test code is located in the path:
```json
IOT_EMASA/api-rest-emasa/api/tests
```

## 4. Database synchronization.

Synchronization with the database is done by means of environment variables that communicate between the db code in the route IOT\_EMASA/api-rest-emasa/drf/settings.py:

	DATABASES = {
		 'default': {
		 'ENGINE': 'django.db.backends.postgresql',
		 'NAME': os.environ.get('POSTGRES\_DB'), 
		 'USER': os.environ.get('POSTGRES\_USER'), 
		 'PASSWORD': os.environ.get('POSTGRES\_PASSWORD'), 
		 'HOST': os.environ.get('POSTGRESQL\_HOST'),
		 }
	}

And a file .env.prod located in the root of the project containing the database data how:

**POSTGRESQL\_HOST=** el hostname de la db, en caso de este proyecto es el nombre del contenedor de persistance

**POSTGRES\_USER=** The data base username

**POSTGRES\_PASSWORD=** The data base password

**POSTGRES\_DB=** The data base name

**POSTGRES\_PORT=** The data base port

My django project settings 
	IOT\_EMASA/api-rest-emasa/drf/settings.py
comunicates with .env.prod thanks to the api container 
	IOT\_EMASA/api-rest-emasa/docker-compose.prod.yml
has it declared.

	Web:
 		 env_file:
 			  - path: ../.env.prod


## 5. Responses and transactions.

#### 5.1. Register Users

**- Description:** User registration from the EMASA API synchronized with ChirpStack.

**- Module:** chirpstack_api.py (función "sync_user_to_chirpstack")

**- Type:** Transaction (2) outgoing


#### 5.2. Register Machines

**- Description:** Device registration from django api to chirpstack.

**- Module:** chirpstackDeviceViewSet

**- Type:** Transaction (2) outgoing


#### 5.3. Boot Notification (Register)

**- Description:** Initial user registration simulated by entity creation.

**- Type:** Transaction (2) outgoing


#### 5.4. Set Machines

**- Description:** Assignment of machines to users/tenants.

**- Module:** 

**- Type:** Transaction (2) outgoing


#### 5.5. SendData

**- Description:** Sending data from EMASA to ChirpStack or the machine (using endpoints or MQTT).

**- Type:** Transaction (2) outgoing


#### 5.6. Data Transfer Request

**- Description:** Data request to a machine or from ChirpStack.

**- Type:** Transaction (2) outgoing


#### 5.7. Diagnostic Status

**- Description:** Diagnostic information exchanged through the function `SendData`.

**- Type:** Transaction (2) outgoing


#### 5.8. Change Availability Request

**- Description:**

**- Module:**

**- Type:** Transaction (2) outgoing


#### 5.9. Stop Transaction Response

**- Description:**

**- Module:**

**- Type:**


#### 5.11. Change Availability Response

**- Description:**

**- Module:**

**- Type:**
