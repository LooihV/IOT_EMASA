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

* asgiref                        3.8.1
* attrs                          25.1.0
* autobahn                       24.4.2
* Automat                        24.8.1
* cffi                           1.17.1
* channels                       4.2.0
* channels_redis                 4.2.1
* constantly                     23.10.4
* cryptography                   44.0.1
* daphne                         4.1.2
* Django                         5.1.6
* django-cors-headers            4.7.0
* djangorestframework            3.15.2
* djangorestframework_simplejwt  5.4.0
* hyperlink                      21.0.0
* idna                           3.10
* incremental                    24.7.2
* jsonschema                     4.23.0
* jsonschema-specifications      2024.10.1
* msgpack                        1.1.0
* ocpp                           2.0.0
* pip                            25.0.1
* psycopg                        3.2.4
* psycopg2-binary                2.9.10
* pyasn1                         0.6.1
* pyasn1_modules                 0.4.1
* pycparser                      2.22
* PyJWT                          2.10.1
* pyOpenSSL                      25.0.0
* redis                          5.2.1
* referencing                    0.36.2
* rpds-py                        0.23.1
* service-identity               24.2.0
* setuptools                     75.8.0
* sqlparse                       0.5.3
* Twisted                        24.11.0
* txaio                          23.1.1
* typing_extensions              4.12.2
* websockets                     15.0
* zope.interface                 7.2

### Despliegue

* <img src="data:image/png;base64,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" width="5" height="5"> Texto después de la imagen
 Database: 'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'dbsens',
            'USER': 'miusuario',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': '5432',

*
