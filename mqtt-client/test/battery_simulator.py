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

# LoRaWAN device configuration
DEV_EUI = "a0102030a4b0c5d0"
DEV_ADDR = "01020304"
NWK_S_KEY = "01020304050607080910111213141516"
APP_S_KEY = "01020304050607080910111213141516"

# Connection configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SEND_INTERVAL = 10  # seconds between messages

APP_ID = "d0f1bf02-0c30-4e05-0b60-70fd80fcd9db"
DEVICE_NAME = "test-device"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def generate_battery_sample():
    """Generate a single battery value sample"""
    timestamp = int(time.time() * 1000)
    battery = round(random.uniform(10.5, 13.5), 2)  # Battery voltage between 3.0V and 4.2V
    iso_time = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
    return {
        "time": timestamp,
        "time_iso": iso_time,
        "value": battery
    }, timestamp

def get_fcnt():
    return random.randint(1, 1000)

try:
    while True:
        battery_value, message_time = generate_battery_sample()
        sample_data = struct.pack(">HH", 201, 1)  # series_id for battery + count=1
        encoded_data = base64.b64encode(sample_data).decode()
        fcnt = get_fcnt()
        payload = {
            "deduplicationId": f"sim-{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(100000000000, 999999999999):012x}",
            "time": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00',
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
                "series_id": 201.0,
                "message_arrival_time": float(message_time),
                "machine_uptime_ms": random.randint(80000000, 90000000),
                "fragment_number": 1.0,
                "machine_start_time": float(message_time - 90000000),
                "measurement": "Battery Voltage",
                "values": [battery_value],
                "type": "battery",
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
        topic = f"v4/device/{APP_ID}/{DEV_EUI}/event/up"
        final_message = json.dumps(payload, indent=2)
        client.publish(topic, final_message)
        print(f"✅ Battery message sent: {topic}")
        print(f"   DevEUI: {DEV_EUI}, FCnt: {fcnt}")
        print(f"   Serie ID: 201, Battery: {battery_value['value']}V")
        print("\n" + "="*60 + "\n")
        time.sleep(SEND_INTERVAL)
except KeyboardInterrupt:
    print("Battery simulation stopped by user")
    client.disconnect()
