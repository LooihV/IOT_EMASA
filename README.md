# 🌐 Proyecto de Administración de Dispositivos IoT

Este proyecto está compuesto por dos componentes principales: una **API REST** desarrollada en **FastAPI** y un **servidor LoRaWAN**, diseñados para trabajar en conjunto y permitir la administración, monitoreo y comunicación con dispositivos IoT. El sistema utiliza un protocolo propio, inspirado en **OCPP 2.1**, adaptado para redes LoRaWAN.

---

## 🚀 Características

- ✅ Registro y autenticación de dispositivos mediante **JWT**.
- 📡 Envío y recepción de comandos para dispositivos IoT a través de un servidor LoRaWAN.
- 📊 Gestión de estados y monitoreo de dispositivos en tiempo real.
- 🔐 Seguridad basada en autenticación por tokens.
- ⚙️ Arquitectura escalable utilizando **FastAPI** y **PostgreSQL**.

---

## 🧠 Tecnologías utilizadas

- **Python** – backend API con DJANGO rest Framework.
- **PostgreSQL** – base de datos relacional.
- **Docker** – contenedores para despliegue ágil y portátil.
- **ChirpStack** – servidor LoRaWAN para gestión de red.
- **Dragino** – dispositivos LoRaWAN compatibles.
- **JWT (JSON Web Tokens)** – autenticación segura.

---

## 📁 Estructura del proyecto

```bash
/mi-proyecto
├── /api_rest_emasa           # API REST con FastAPI
│   ├── main.py
│   └── ...
├── /lorawan_server        # Servidor LoRaWAN e integración con ChirpStack
│   └── ...
├── LICENSE
└── README.md

```

---
## Librerías y paquetes

- asgiref==3.8.1
- attrs==25.1.0
- autobahn==24.4.2
- Automat==24.8.1
- cffi==1.17.1
- channels==4.2.0
- channels_redis==4.2.1
- constantly==23.10.4
- cryptography==44.0.1
- daphne==4.1.2
- dj-database-url==2.3.0
- Django==5.1.6
- django-cors-headers==4.7.0
- djangorestframework==3.15.2
- requests
- djangorestframework_simplejwt==5.4.0
- hyperlink==21.0.0
- idna==3.10
- incremental==24.7.2
- jsonschema==4.23.0
- jsonschema-specifications==2024.10.1
- msgpack==1.1.0
- ocpp==2.0.0
- psycopg==3.2.4
- psycopg2-binary==2.9.10
- pyasn1==0.6.1
- pyasn1_modules==0.4.1
- pycparser==2.22
- PyJWT==2.10.1
- pyOpenSSL==25.0.0
- redis==5.2.1
- referencing==0.36.2
- rpds-py==0.23.1
- service-identity==24.2.0
- setuptools==75.8.0
- sqlparse==0.5.3
- Twisted==24.11.0
- txaio==23.1.1
- typing_extensions==4.12.2
- websockets==15.0
- zope.interface==7.2
- whitenoise==6.6.0
