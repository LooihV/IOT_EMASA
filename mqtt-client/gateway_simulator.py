import paho.mqtt.client as mqtt
import json
import base64
import time
import random
import struct
import binascii
from datetime import datetime

# Configuración del gateway
GATEWAY_ID = "a0102030a4b0c5d0"  # ID del gateway simulado
PHY_PAYLOAD = ""  # Carga física de LoRaWAN (opcional para simulación completa)

# Configuración del dispositivo
DEV_EUI = "a0102030a4b0c5d0"
DEV_ADDR = "01020304"

# Configuración de conexión
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SEND_INTERVAL = 10  # segundos

# Crear cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    while True:
        # Simular datos del sensor
        temperature = round(random.uniform(20.0, 30.0), 1)
        humidity = round(random.uniform(40.0, 80.0), 1)
        light = random.randint(100, 1000)
        
        # Empaquetar datos
        sensor_data = struct.pack(">ffH", temperature, humidity, light)
        encoded_data = base64.b64encode(sensor_data).decode()
        
        # ID único para la transmisión
        uplink_id = f"{int(time.time())}-{random.randint(1000, 9999)}"
        
        # Construir payload en formato gateway ChirpStack v4
        gateway_payload = {
            "phyPayload": encoded_data,  # Normalmente sería el payload LoRaWAN completo
            "txInfo": {
                "frequency": 868300000,
                "modulation": {
                    "lora": {
                        "bandwidth": 125000,
                        "spreadingFactor": 7,
                        "codeRate": "4/5"
                    }
                }
            },
            "rxInfo": {
                "gatewayId": GATEWAY_ID,
                "uplinkId": uplink_id,
                "rssi": random.randint(-120, -60),
                "snr": random.uniform(5.0, 10.0),
                "channel": 2,
                "location": {
                    "latitude": 52.3740,
                    "longitude": 4.9144
                },
                "context": base64.b64encode(b"gateway-context").decode(),
                "metadata": {
                    "region_name": "eu868",
                    "region_common_name": "EU868"
                }
            }
        }
        
        # Tema MQTT para mensajes de gateway en ChirpStack v4
        gateway_topic = f"v4/gw/{GATEWAY_ID}/event/up"
        
        # Publicar mensaje
        client.publish(gateway_topic, json.dumps(gateway_payload))
        
        print(f"✅ Mensaje de gateway enviado: {gateway_topic}")
        print(f"   GatewayID: {GATEWAY_ID}, UplinkID: {uplink_id}")
        print(f"   Simulando datos: Temp={temperature}°C, Humedad={humidity}%, Luz={light} lux")
        
        # Crear mensaje de estadísticas del gateway para aparecer como "online"
        stats_payload = {
            "gatewayId": GATEWAY_ID,
            "time": datetime.now().isoformat() + "Z",
            "location": {
                "latitude": 52.3740,
                "longitude": 4.9144
            },
            "configVersion": "1.0.0",
            "rx_packets_received": random.randint(10, 50),
            "rx_packets_received_ok": random.randint(10, 50),
            "tx_packets_received": random.randint(5, 20),
            "tx_packets_emitted": random.randint(5, 20)
        }

        # Publicar estadísticas
        stats_topic = f"v4/gw/{GATEWAY_ID}/event/stats"
        client.publish(stats_topic, json.dumps(stats_payload))
        print(f"📊 Estadísticas de gateway enviadas: {stats_topic}")
        
        time.sleep(SEND_INTERVAL)
        
except KeyboardInterrupt:
    print("Simulación detenida por el usuario")
    client.disconnect()