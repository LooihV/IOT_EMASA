import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import ssl
import json
import base64
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.info("MQTT client starting up...")

def on_connect(client, userdata, flags, reason_code, properties=None):
    logging.info(f"✅ Connected with result code: {reason_code}")
    client.subscribe("application/+/device/+/event/up")
    client.subscribe("us915_7/gateway/+/event/stats")

"""def on_message(client, userdata, msg):
    logging.info(f"[MQTT V5] {msg.topic} → {msg.payload.decode()}")
    """
def on_message(client, userdata, msg):
    logging.info(f"[MQTT] Topic: {msg.topic}")
    
    try:
        # Intenta decodificar como UTF-8 (para mensajes JSON)
        payload = msg.payload.decode()
        data = json.loads(payload)
        
        # Procesa los datos JSON normalmente
        if "data" in data:
            b = base64.b64decode(data["data"])
            logging.info(f"Raw bytes (from JSON): {b}")
        else:
            logging.warning(f"JSON recibido sin campo 'data': {data}")
            
    except UnicodeDecodeError:
        # Si falla como UTF-8, trata el mensaje como binario
        logging.info(f"Mensaje binario recibido: {len(msg.payload)} bytes")
        logging.info(f"Primeros 10 bytes: {msg.payload[:10].hex()}")
        
        # Intentar procesar como binario directo si es necesario
        try:
            # Si el binario podría ser base64 directamente
            raw_data = msg.payload
            logging.info(f"Datos binarios: {raw_data}")
        except Exception as e:
            logging.error(f"Error procesando datos binarios: {e}")
            
    except json.JSONDecodeError:
        # Si es texto pero no JSON válido
        logging.error(f"Mensaje de texto no-JSON recibido: {msg.payload}")
# Create MQTT client with MQTTv5 protocol
client = mqtt.Client(
    callback_api_version=CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv5
)
# Set TLS configuration
"""client.tls_set(
    ca_certs="/etc/paho-mqtt/certs/ca.crt",
    certfile="/etc/paho-mqtt/certs/cert.crt",
    keyfile="/etc/paho-mqtt/certs/cert.key",
    tls_version=ssl.PROTOCOL_TLSv1_2  # Explicit is better than implicit
)"""

# Optional: disable hostname check if using Docker internal hostnames
#client.tls_insecure_set(True)  # ⚠️ For dev only — remove for prod with valid certs

# Attach callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect using the Docker service name and TLS port 8883
client.connect("lorawan-server-mosquitto-1", 1883, 60)

# Start network loop
client.loop_forever()

