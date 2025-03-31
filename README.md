# IOT_EMASA

## API REST para IoT

### 🚀 Descripción

Esta API REST permite la comunicación y gestión de dispositivos IoT utilizando un protocolo propio inspirado en OCPP 2.1. Proporciona endpoints para el registro, autenticación, monitoreo y control remoto de dispositivos conectados en plantas.

### 📌 Características

* 📡 Registro y autenticación de dispositivos mediante JWT.
  
* 🔄 Envío y recepción de comandos para dispositivos IoT.

* 📊 Gestión de estados y monitoreo en tiempo real.

* 🔒 Seguridad con autenticación basada en tokens.

* ⚡ Optimizado para escalabilidad con FastAPI y PostgreSQL.

### 🏗 Tecnologías Utilizadas

* Backend: FastAPI (Python)

* Base de Datos: PostgreSQL / SQLite

* Autenticación: JWT (JSON Web Tokens)

* Docker: Para despliegue en entornos productivos

Protocolos: HTTP / WebSockets (para comunicación bidireccional)

### Librerías Utilizadas

* asgiref==3.8.1
* attrs==25.1.0
* autobahn==24.4.2
* Automat==24.8.1
* cffi==1.17.1
* channels==4.2.0
* channels_redis==4.2.1
* constantly==23.10.4
* cryptography==44.0.1
* daphne==4.1.2
* dj-database-url==2.3.0
* Django==5.1.6
* django-cors-headers==4.7.0
* djangorestframework==3.15.2
* djangorestframework_simplejwt==5.4.0
* hyperlink==21.0.0
* idna==3.10
* incremental==24.7.2
* jsonschema==4.23.0
* jsonschema-specifications==2024.10.1
* msgpack==1.1.0
* ocpp==2.0.0
* psycopg==3.2.4
* psycopg2-binary==2.9.10
* pyasn1==0.6.1
* pyasn1_modules==0.4.1
* pycparser==2.22
* PyJWT==2.10.1
* pyOpenSSL==25.0.0
* redis==5.2.1
* referencing==0.36.2
* rpds-py==0.23.1
* service-identity==24.2.0
* setuptools==75.8.0
* sqlparse==0.5.3
* Twisted==24.11.0
* txaio==23.1.1
* typing_extensions==4.12.2
* websockets==15.0
* zope.interface==7.2
* whitenoise==6.6.0
  
### Despliegue

#### 1) Tener instalado:
1. Python 3.10
2. PostgreSQL V 16
3. Git
4. Virtualenv
5. Redis V 7,4

#### 2) Clonar el repositorio.

#### 3) Crear y activar el ambiente virtual:    
1. python3 -m venv venv
2. source venv/bin/activate  # En Linux/macOS
3. venv\Scripts\activate  # En Windows
     
#### 4) Instalar dependencias:
1. pip install -r requirements.txt
2. pip freeze > requirements.txt

#### 5) Configurar PostgreSQL:
1. sudo -u postgres psql
2. CREATE DATABASE dbsens;
3. CREATE USER miusuario WITH PASSWORD 'admin';
4. ALTER ROLE miusuario SET client_encoding TO 'utf8';
5. ALTER ROLE miusuario SET default_transaction_isolation TO 'read committed';
6. ALTER ROLE miusuario SET timezone TO 'UTC';
7. GRANT ALL PRIVILEGES ON DATABASE dbsens TO miusuario;

#### 6) Configurar variables del entorno virtual:
1. Crear un archivo .env en la raiz del proyecto
2. DJANGO_SECRET_KEY='clave-super-segura'
3. DJANGO_DEBUG=True
4. DB_NAME=dbsens
5. DB_USER=miusuario
6. DB_PASSWORD=admin
7. DB_HOST=localhost
8. DB_PORT=5432

#### 7) Ejecutar y Utilizar las migraciones:
1. python manage.py makemigrations
2. python manage.py migrate

#### 8) Levantar la API el servidor local:
1. python manage.py runserver 8000
 
#### 9) Endpoints de la API:
1. http://localhost:8000/admin/
2. http://localhost:8000/api/v1/Users/
3. http://localhost:8000/api/v1/Maquinas/
4. http://localhost:8000/api/v1/Registro/


