import datetime
import paho.mqtt.client as mqtt
import json
import base64
import time
import random
import struct
import binascii
import os

# Environment variables for MQTT credentials
mqtt_username = os.getenv("MQTT_USERNAME", "admin")
mqtt_password = os.getenv("MQTT_PASSWORD", "admin")

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
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def generate_voltage_series():
    """Genera una serie temporal de voltajes simulados"""
    base_time = int(time.time() * 1000)  # timestamp en ms
    values = []
    
    # Generar 50 puntos de datos (como tu ejemplo real)
    for i in range(150):
        timestamp = base_time + (i * 300)  # cada 300ms
        voltage = round(random.uniform(0.5, 5.0), 1)  # Voltaje entre 0.5V y 5V
        
        iso_time = datetime.datetime.fromtimestamp(timestamp/1000, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
        
        values.append({
            "time": timestamp,
            "time_iso": iso_time,
            "value": voltage
        })
    
    return values, base_time

def get_fcnt():
    """Simula contador de tramas que incrementa con cada mensaje"""
    return random.randint(1, 1000)

try:
    while True:
        # Generar datos de voltaje
        voltage_values, message_time = generate_voltage_series()
        
        # Crear payload compacto (similar a tu data real pero más simple)
        # En el ejemplo real, 'data' parece ser una codificación binaria compleja
        sample_data = struct.pack(">HH", 151, len(voltage_values))  # series_id + count
        encoded_data = base64.b64encode(sample_data).decode()
        
        fcnt = get_fcnt()
        
        # Payload en formato ChirpStack v4 (basado en tu JSON)
        payload = {
            "deduplicationId": f"sim-{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(100000000000, 999999999999):012x}",
            "time": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00',
            "deviceInfo": {
                "tenantId": "1c27c2fb-d0d6-4883-9b19-d76a0821ed28",
                "tenantName": "POTENCIA",
                "applicationId": APP_ID,
                "applicationName": "delapotenmcia",
                "deviceProfileId": "2742c266-f0e5-45cb-a7dd-6db0165ba2eb",
                "deviceProfileName": "profile-device",
                "deviceName": DEVICE_NAME,
                "devEui": DEV_EUI,
                "deviceClassEnabled": "CLASS_A",
                "tags": {}
            },
            "devAddr": DEV_ADDR,
            "adr": False,
            "dr": 3,
            "fCnt": fcnt,
            "fPort": 1,
            "confirmed": False,
            "data": encoded_data,
            "object": {
                "series_id": 151.0,
                "message_arrival_time": float(message_time),
                "machine_uptime_ms": random.randint(80000000, 90000000),
                "fragment_number": 1.0,
                "machine_start_time": float(message_time - 90000000),
                "measurement": "Volts RMS",
                "values": voltage_values,
                "type": "voltage",
                "total_fragments": 1.0
            },
            "rxInfo": [{
                "gatewayId": "a84041fdfe2764b6",
                "uplinkId": random.randint(8000, 9000),
                "gwTime": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00',
                "nsTime": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00',
                "rssi": random.randint(-15, -5),
                "snr": round(random.uniform(10.0, 15.0), 1),
                "channel": random.randint(0, 7),
                "rfChain": 1,
                "location": {},
                "context": "eMnGgA==",
                "crcStatus": "CRC_OK"
            }],
            "txInfo": {
                "frequency": 914900000,
                "modulation": {
                    "lora": {
                        "bandwidth": 125000,
                        "spreadingFactor": 7,
                        "codeRate": "CR_4_5"
                    }
                }
            },
            "regionConfigId": "us915_7"
        }
        
        # Publicar mensaje
        topic = f"v4/device/{APP_ID}/{DEV_EUI}/event/up"
        final_message = json.dumps(payload, indent=2)
        
        client.publish(topic, final_message)
        
        print(f"✅ Mensaje enviado: {topic}")
        print(f"   DevEUI: {DEV_EUI}, FCnt: {fcnt}")
        print(f"   Serie ID: 151, Mediciones: {len(voltage_values)} valores")
        print(f"   Rango de voltaje: {min(v['value'] for v in voltage_values):.1f}V - {max(v['value'] for v in voltage_values):.1f}V")
        print("\n" + "="*60 + "\n")
        
        # Esperar para el siguiente envío
        time.sleep(SEND_INTERVAL)
        
except KeyboardInterrupt:
    print("Simulación detenida por el usuario")
    client.disconnect()