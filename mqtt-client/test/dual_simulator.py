"""
Dual LoRaWAN Device Simulator (Voltage & Current)

This module simulates two LoRaWAN devices that alternately send voltage and current
measurements. Designed for testing dual-chart frontend applications and validating
multi-device IoT data processing pipelines.

Key Features:
- Dual device simulation (voltage + current monitoring)
- Alternating message transmission between devices
- ChirpStack v4 protocol compliance
- Realistic time-series data generation
- Independent device configurations

Use Cases:
- Multi-device frontend testing
- Load testing with multiple data streams
- Dual-chart application validation
- Device switching behavior simulation

Author: IoT Development Team
Version: 1.0
Date: August 2025
"""

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

# Dual LoRaWAN device configuration
DEV_EUI_VOLTAGE = "a0102030a4b0c5d0"  # Voltage device identifier (8 bytes hex)
DEV_EUI_CURRENT = "a0102030a4b0c5d1"  # Current device identifier (8 bytes hex)
DEV_ADDR_VOLTAGE = "01020304"         # Voltage device network address (4 bytes hex)
DEV_ADDR_CURRENT = "01020305"         # Current device network address (4 bytes hex)
NWK_S_KEY = "01020304050607080910111213141516"  # Network Session Key (16 bytes hex)
APP_S_KEY = "01020304050607080910111213141516"  # Application Session Key (16 bytes hex)

# MQTT connection configuration
MQTT_BROKER = os.getenv("MQTT_BROKER_HOST", "localhost")  # Use environment variable
MQTT_PORT = 1883
SEND_INTERVAL = 8  # seconds between messages (faster for dual simulation)

# ChirpStack application configuration
APP_ID = "d0f1bf02-0c30-4e05-0b60-70fd80fcd9db"       # Application ID in ChirpStack

"""
Initialize MQTT client for dual device simulation.
"""
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

"""
Generate voltage measurement time-series.

Creates 50 voltage readings with 300ms intervals for industrial
voltage monitoring simulation.

Returns:
    tuple: (voltage_values, base_timestamp)
        - voltage_values: List of voltage readings (0.5V-5.0V)
        - base_timestamp: Base timestamp in milliseconds
"""
def generate_voltage_series():
    
    base_time = int(time.time() * 1000)
    values = []
    
    for i in range(50):
        timestamp = base_time + (i * 300)  # 300ms intervals
        voltage = round(random.uniform(0.5, 5.0), 1)  # 0.5V-5.0V range
        
        iso_time = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
        
        values.append({
            "time": timestamp,
            "time_iso": iso_time,
            "value": voltage
        })
    
    return values, base_time

"""
Generate current measurement time-series.

Creates 50 current readings with 300ms intervals for industrial
current monitoring simulation.

Returns:
    tuple: (current_values, base_timestamp)
        - current_values: List of current readings (0.1A-2.5A)
        - base_timestamp: Base timestamp in milliseconds
"""
def generate_current_series():
    
    base_time = int(time.time() * 1000)
    values = []
    
    for i in range(50):
        timestamp = base_time + (i * 300)  # 300ms intervals
        current = round(random.uniform(0.1, 2.5), 2)  # 0.1A-2.5A range
        
        iso_time = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
        
        values.append({
            "time": timestamp,
            "time_iso": iso_time,
            "value": current
        })
    
    return values, base_time

"""
Generate LoRaWAN frame counter.

Returns:
    int: Random frame counter (1-1000) for protocol simulation
"""
def get_fcnt():
    
    return random.randint(1, 1000)

"""
Send measurement data for specified device type.

Creates and publishes a complete ChirpStack v4 message for either
voltage or current device with appropriate configuration.

Args:
    measurement_type (str): "voltage" or "current"
        - voltage: Sends voltage data with series_id 151
        - current: Sends current data with series_id 152

Device Configuration:
    Voltage Device:
        - DevEUI: a0102030a4b0c5d0
        - Series ID: 151
        - Range: 0.5V-5.0V
        - Unit: Volts RMS
        
    Current Device:
        - DevEUI: a0102030a4b0c5d1
        - Series ID: 152
        - Range: 0.1A-2.5A
        - Unit: Amps RMS

Message Structure:
    - Complete ChirpStack v4 format
    - Device-specific metadata
    - 50-sample time-series data
    - Radio parameters (RSSI, SNR)
    - Binary payload encoding
"""
def send_measurement(measurement_type):
    
    # Configure device-specific parameters
    if measurement_type == "voltage":
        values, message_time = generate_voltage_series()
        dev_eui = DEV_EUI_VOLTAGE
        dev_addr = DEV_ADDR_VOLTAGE
        device_name = "test-device-voltage"
        series_id = 151.0
        measurement_unit = "Volts RMS"
        unit_symbol = "V"
    else:  # current
        values, message_time = generate_current_series()
        dev_eui = DEV_EUI_CURRENT
        dev_addr = DEV_ADDR_CURRENT
        device_name = "test-device-current"
        series_id = 152.0
        measurement_unit = "Amps RMS"
        unit_symbol = "A"
    
    # Create binary payload with device metadata
    sample_data = struct.pack(">HH", int(series_id), len(values))  # series_id + count
    encoded_data = base64.b64encode(sample_data).decode()
    
    fcnt = get_fcnt()
    
    # Build ChirpStack v4 compliant message
    payload = {
        "deduplicationId": f"sim-{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(100000000000, 999999999999):012x}",
        "time": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00',
        
        # Device-specific information
        "deviceInfo": {
            "tenantId": "1c27c2fb-d0d6-4883-9b19-d76a0821ed28",
            "tenantName": "POTENCIA",
            "applicationId": APP_ID,
            "applicationName": "delapotenmcia",
            "deviceProfileId": "2742c266-f0e5-45cb-a7dd-6db0165ba2eb",
            "deviceProfileName": "profile-device",
            "deviceName": device_name,
            "devEui": dev_eui,
            "deviceClassEnabled": "CLASS_A",
            "tags": {}
        },
        
        # LoRaWAN protocol parameters
        "devAddr": dev_addr,
        "adr": False,
        "dr": 3,
        "fCnt": fcnt,
        "fPort": 1,
        "confirmed": False,
        "data": encoded_data,
        
        # Decoded measurement data
        "object": {
            "series_id": series_id,
            "message_arrival_time": float(message_time),
            "machine_uptime_ms": random.randint(80000000, 90000000),
            "fragment_number": 1.0,
            "machine_start_time": float(message_time - 90000000),
            "measurement": measurement_unit,
            "values": values,
            "type": measurement_type,
            "total_fragments": 1.0
        },
        
        # Radio reception parameters
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
        
        # Transmission parameters
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
    
    # Publish device-specific message
    topic = f"v4/device/{APP_ID}/{dev_eui}/event/up"
    final_message = json.dumps(payload, indent=2)
    
    client.publish(topic, final_message)
    
    # Log transmission with device-specific details
    print(f"✅ {measurement_type.upper()} message sent: {topic}")
    print(f"   DevEUI: {dev_eui}, FCnt: {fcnt}")
    print(f"   Series ID: {int(series_id)}, Measurements: {len(values)} values")
    print(f"   Range: {min(v['value'] for v in values):.2f}{unit_symbol} - {max(v['value'] for v in values):.2f}{unit_symbol}")
    print("\n" + "="*60 + "\n")

"""
Main dual simulation loop.

Alternates between voltage and current device transmissions,
simulating a complete dual-device monitoring system.

Transmission Pattern:
- Message 0, 2, 4... : Voltage device
- Message 1, 3, 5... : Current device
- 8-second intervals between messages
- Continuous operation until interrupted

Error Handling:
- KeyboardInterrupt: Graceful shutdown with MQTT disconnect
"""
try:
    message_count = 0
    while True:
        # Alternate between voltage and current devices
        measurement_type = "voltage" if message_count % 2 == 0 else "current"
        send_measurement(measurement_type)
        
        message_count += 1
        
        # Wait for next transmission cycle
        time.sleep(SEND_INTERVAL)
        
except KeyboardInterrupt:
    """
    Handle graceful shutdown for dual simulation.
    """
    print("🛑 Dual simulation stopped by user")
    client.disconnect()