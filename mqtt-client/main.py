import paho.mqtt.client as mqtt
import ssl

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"✅ Connected with result code: {reason_code}")
    client.subscribe("application/+/device/+/event/up")

def on_message(client, userdata, msg):
    print(f"[MQTT V5] {msg.topic} → {msg.payload.decode()}")

# Create MQTT client with MQTTv5 protocol
client = mqtt.Client(protocol=mqtt.MQTTv5)

# Set TLS configuration
client.tls_set(
    ca_certs="/etc/paho-mqtt/certs/ca.crt",
    certfile="/etc/paho-mqtt/certs/cert.crt",
    keyfile="/etc/paho-mqtt/certs/cert.key",
    tls_version=ssl.PROTOCOL_TLSv1_2  # Explicit is better than implicit
)

# Optional: disable hostname check if using Docker internal hostnames
client.tls_insecure_set(True)  # ⚠️ For dev only — remove for prod with valid certs

# Attach callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect using the Docker service name and TLS port 8883
client.connect("lorawan-server-mosquitto-1", 8883, 60)

# Start network loop
client.loop_forever()

