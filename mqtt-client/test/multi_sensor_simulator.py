import datetime
import paho.mqtt.client as mqtt
import json
import base64
import time
import random
import struct
import os

# Environment variables for MQTT credentials
mqtt_username = os.getenv("MQTT_USERNAME", "admin")
mqtt_password = os.getenv("MQTT_PASSWORD", "admin")

# LoRaWAN device configuration
DEV_EUI = "a0102030a4b0c5d0"
DEV_ADDR = "01020304"

# Connection configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SEND_INTERVAL = 15  # seconds between messages

APP_ID = "d0f1bf02-0c30-4e05-0b60-70fd80fcd9db"
DEVICE_NAME = "multi-sensor-device"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def generate_voltage_samples(num_samples=30):
    """Generate voltage samples for multiple channels."""
    base_time = int(time.time() * 1000)
    
    # Channel 1 - Higher voltage
    ch1_samples = []
    for i in range(num_samples):
        timestamp = base_time + (i * 200)  # every 200ms
        voltage = round(random.uniform(220.0, 240.0), 2)
        iso_time = datetime.datetime.fromtimestamp(timestamp/1000, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
        ch1_samples.append({
            "value": voltage,
            "time": iso_time
        })
    
    # Channel 2 - Lower voltage
    ch2_samples = []
    for i in range(num_samples):
        timestamp = base_time + (i * 200)
        voltage = round(random.uniform(110.0, 125.0), 2)
        iso_time = datetime.datetime.fromtimestamp(timestamp/1000, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
        ch2_samples.append({
            "value": voltage,
            "time": iso_time
        })
    
    return ch1_samples, ch2_samples, base_time

def generate_current_samples(num_samples=25):
    """Generate current samples for channel 1."""
    base_time = int(time.time() * 1000)
    
    ch1_samples = []
    for i in range(num_samples):
        timestamp = base_time + (i * 300)
        current = round(random.uniform(5.0, 85.0), 2)
        iso_time = datetime.datetime.fromtimestamp(timestamp/1000, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
        ch1_samples.append({
            "value": current,
            "time": iso_time
        })
    
    return ch1_samples, base_time

def get_fcnt():
    """Simulate frame counter"""
    return random.randint(1, 1000)

try:
    while True:
        voltage_ch1, voltage_ch2, voltage_time = generate_voltage_samples()
        current_ch1, current_time = generate_current_samples()
        
        reference_time = min(voltage_time, current_time)
        
        sample_data = struct.pack(">H", 999)
        encoded_data = base64.b64encode(sample_data).decode()

        fcnt = get_fcnt()

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
                "id": random.randint(1000, 9999),
                "relative_timestamp": int(reference_time / 1000),
                "arrival_date": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                "active_sensors": ["voltage", "current"],
                "measurements": {
                    "voltage": {
                        "cha1": voltage_ch1,
                        "ch2": voltage_ch2
                    },
                    "current": {
                        "cha1": current_ch1
                    }
                }
            },
            "rxInfo": [{
                "gatewayId": "a84041fdfe2764b6",
                "uplinkId": random.randint(8000, 9000),
                "gwTime": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00',
                "nsTime": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00',
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

        topic = f"applications/{APP_ID}/devices/{DEV_EUI}/event/up"
        final_message = json.dumps(payload, indent=2)

        client.publish(topic, final_message)

        print(f"✅ Multi-sensor message sent: {topic}")
        print(f"   DevEUI: {DEV_EUI}, FCnt: {fcnt}")
        print(f"   ID: {payload['object']['id']}")
        print(f"   Active sensors: {', '.join(payload['object']['active_sensors'])}")
        print(f"   Voltage CH1: {len(voltage_ch1)} samples ({min(v['value'] for v in voltage_ch1):.1f}V - {max(v['value'] for v in voltage_ch1):.1f}V)")
        print(f"   Voltage CH2: {len(voltage_ch2)} samples ({min(v['value'] for v in voltage_ch2):.1f}V - {max(v['value'] for v in voltage_ch2):.1f}V)")
        print(f"   Current CH1: {len(current_ch1)} samples ({min(v['value'] for v in current_ch1):.1f}A - {max(v['value'] for v in current_ch1):.1f}A)")
        print("\n" + "="*70 + "\n")

        time.sleep(SEND_INTERVAL)

except KeyboardInterrupt:
    print("Multi-sensor simulation stopped by user")
    client.disconnect()
