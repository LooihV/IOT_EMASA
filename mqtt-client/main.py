import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado con código: " + str(rc))
    client.subscribe("application/+/device/+/event/up")

def on_message(client, userdata, msg):
    print(f"[MQTT] {msg.topic} → {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Si usas TLS
client.tls_set(
    ca_certs="/certs/ca.pem",
    certfile="/certs/client.crt",
    keyfile="/certs/client.key"
)

client.connect("mosquitto", 8883, 60)  # Usa el nombre del contenedor del broker

client.loop_forever()