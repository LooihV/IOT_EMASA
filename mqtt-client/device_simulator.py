import datetime
import paho.mqtt.client as mqtt
import json
import base64
import time
import random
import struct
import binascii

# Configuración del dispositivo LoRaWAN

DEV_EUI = "a0102030a4b0c5d0"  # Identificador único del dispositivo (8 bytes hex)
DEV_ADDR = "01020304"         # Dirección del dispositivo (4 bytes hex)
NWK_S_KEY = "01020304050607080910111213141516"  # Network Session Key (16 bytes hex)
APP_S_KEY = "01020304050607080910111213141516"  # Application Session Key (16 bytes hex)

# Configuración de la conexión
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SEND_INTERVAL = 10  # segundos entre mensajes

# Identificación

APP_ID = "d0f1bf02-0c30-4e05-0b60-70fd80fcd9db"       # ID de la aplicación en ChirpStack
DEVICE_NAME = "test-device"  # Nombre amigable del dispositivo

# Crear cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def get_fcnt():
    """Simula contador de tramas que incrementa con cada mensaje"""
    return random.randint(1, 1000)

try:
    while True:
        # Simular lecturas de sensores
        temperature = round(random.uniform(20.0, 30.0), 1)
        humidity = round(random.uniform(40.0, 80.0), 1)
        light = random.randint(100, 1000)
        
        # Codificar datos como lo haría un dispositivo real
        sensor_data = struct.pack(">ffH", temperature, humidity, light)
        
        # Codificar en Base64 como haría un dispositivo LoRaWAN
        encoded_data = base64.b64encode(sensor_data).decode()
        
        # Construir payload en formato ChirpStack
        fcnt = get_fcnt()
        ppayload = {
    "deduplicationId": "random-id-" + str(random.randint(10000, 99999)),
    "time": datetime.now().isoformat() + "Z",
    "deviceInfo": {
        "tenantId": "tenant-id",
        "tenantName": "tenant-name",
        "applicationId": APP_ID,
        "applicationName": "test",
        "deviceProfileId": "device-profile-id",
        "deviceProfileName": "test-profile",
        "deviceName": DEVICE_NAME,
        "devEui": DEV_EUI
    },
    "devAddr": DEV_ADDR,
    "adr": True,
    "dr": 3,
    "fCnt": fcnt,
    "fPort": 1,
    "data": encoded_data,
    "rxInfo": [{
        "gatewayId": "a0102030a4b0c5d0",
        "uplinkId": random.randint(1000000, 9999999),
        "rssi": random.randint(-120, -60),
        "snr": random.uniform(5.0, 10.0),
        "channel": 2,
        "location": {
            "latitude": 52.3740,
            "longitude": 4.9144
        }
    }],
    "object": {
        "temperature": temperature,
        "humidity": humidity,
        "light": light
    }
}
        
        # Publicar mensaje en el formato que ChirpStack espera
        topic = f"v4/device/{APP_ID}/{DEV_EUI}/event/up"
        client.publish(topic, json.dumps(payload))
        
        print(f"✅ Mensaje enviado: {topic}")
        print(f"   DevEUI: {DEV_EUI}, FCnt: {fcnt}")
        print(f"   Datos: Temp={temperature}°C, Humedad={humidity}%, Luz={light} lux")
        
        # Esperar para el siguiente envío
        time.sleep(SEND_INTERVAL)
        
except KeyboardInterrupt:
    print("Simulación detenida por el usuario")
    client.disconnect()