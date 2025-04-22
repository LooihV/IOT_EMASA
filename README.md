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
├── /api_rest_emasa           # API REST con DJANGO rest Framework
│   ├── main.py
│   └── ...
├── /lorawan_server        # Servidor LoRaWAN e integración con ChirpStack
│   └── ...
├── LICENSE
└── README.md

