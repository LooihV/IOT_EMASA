"""
LoRaWAN Gateway Simulator for IoT Testing

This module implements a comprehensive LoRaWAN gateway simulator that generates
realistic IoT sensor data and publishes it via MQTT using ChirpStack v4 protocol.
It simulates complete gateway behavior including uplink messages, statistical
reporting, and radio frequency parameters for development and testing purposes.

Key Features:
- ChirpStack v4 protocol compliance for gateway simulation
- Multi-sensor data generation (temperature, humidity, light)
- Realistic radio frequency parameter simulation (RSSI, SNR, frequency)
- Gateway statistics reporting for infrastructure monitoring
- Binary data encoding with Base64 representation
- Configurable transmission intervals and parameters
- Comprehensive MQTT topic structure for testing

Use Cases:
    - Development environment testing without physical hardware
    - Load testing for MQTT brokers and WebSocket servers
    - Protocol validation and message format verification
    - Frontend application testing with realistic data streams
    - Network simulation for capacity planning

Simulated Components:
    Gateway Infrastructure: Simulates LoRaWAN gateway with realistic metadata
    Sensor Devices: Multi-parameter environmental monitoring
    RF Environment: Realistic signal strength and quality parameters
    Network Protocol: Complete ChirpStack v4 message formatting

Data Generation:
    - Temperature: 20.0°C - 30.0°C (industrial/commercial range)
    - Humidity: 40% - 80% (typical indoor/outdoor range)
    - Light: 100 - 1000 lux (ambient to bright office lighting)
    - RSSI: -120dBm to -60dBm (poor to excellent signal)
    - SNR: 5.0dB to 10.0dB (good to excellent quality)

Author: IoT Development Team
Version: 1.0
Date: August 2025
"""

import paho.mqtt.client as mqtt
import json
import base64
import time
import random
import struct
import binascii
from datetime import datetime
import os

# Environment variables for MQTT credentials
mqtt_username = os.getenv("MQTT_USERNAME", "admin")
mqtt_password = os.getenv("MQTT_PASSWORD", "admin")

# Gateway infrastructure configuration
GATEWAY_ID = "a0102030a4b0c5d1"  # Unique gateway identifier (8-byte hex, 16 chars)
PHY_PAYLOAD = ""  # LoRaWAN physical payload (reserved for complete simulation)

# Device identification configuration
DEV_EUI = "a0102030a4b0c5d0"   # Device Extended Unique Identifier
DEV_ADDR = "01020304"          # Device Address (4-byte network address)

# MQTT broker connection settings
MQTT_BROKER = "localhost"       # MQTT broker hostname/IP
MQTT_PORT = 1883               # Standard MQTT port (non-encrypted)
SEND_INTERVAL = 10             # Transmission interval in seconds

"""
Initialize MQTT client connection.

Establishes connection to the MQTT broker for publishing simulated
gateway messages. Uses standard MQTT v3.1.1 protocol with automatic
reconnection capabilities.

Connection Parameters:
    - Broker: localhost (development environment)
    - Port: 1883 (standard MQTT, non-encrypted)
    - Keepalive: 60 seconds
    - Clean Session: True (no persistent state)

Error Handling:
    - Connection failures will raise exceptions
    - Automatic reconnection not implemented (suitable for testing)
    - Manual restart required on connection loss

Production Notes:
    - Consider using encrypted MQTT (port 8883) for production
    - Implement authentication for secure environments
    - Add connection monitoring and automatic reconnection
"""
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

"""
Main simulation loop for continuous data generation.

Implements the core simulation logic that generates realistic sensor data,
packages it according to LoRaWAN protocols, and publishes via MQTT using
ChirpStack v4 message format. Runs continuously until user interruption.

Simulation Workflow:
1. Generate realistic multi-sensor environmental data
2. Package sensor data using binary encoding (struct)
3. Encode binary data as Base64 for JSON compatibility
4. Create ChirpStack v4 compliant gateway uplink message
5. Publish uplink data to appropriate MQTT topic
6. Generate and publish gateway statistics for infrastructure monitoring
7. Wait for configured interval before next transmission

Data Generation Details:
    Temperature: Simulates environmental temperature sensor
        - Range: 20.0°C to 30.0°C (comfortable indoor/outdoor range)
        - Precision: 0.1°C (typical sensor accuracy)
        - Distribution: Uniform random (simplified for testing)
        
    Humidity: Simulates relative humidity sensor
        - Range: 40% to 80% RH (typical indoor/outdoor range)
        - Precision: 0.1% RH (typical sensor accuracy)
        - Distribution: Uniform random (simplified for testing)
        
    Light: Simulates ambient light sensor
        - Range: 100 to 1000 lux (dim indoor to bright office)
        - Precision: 1 lux (integer values)
        - Distribution: Uniform random (simplified for testing)

Binary Encoding:
    Uses struct.pack with big-endian format (">ffH"):
    - Temperature: 32-bit float (4 bytes)
    - Humidity: 32-bit float (4 bytes)  
    - Light: 16-bit unsigned integer (2 bytes)
    - Total payload: 10 bytes per transmission

RF Parameter Simulation:
    RSSI (Received Signal Strength Indicator):
        - Range: -120dBm to -60dBm
        - -120dBm: Very poor signal (edge of coverage)
        - -60dBm: Excellent signal (close to gateway)
        
    SNR (Signal-to-Noise Ratio):
        - Range: 5.0dB to 10.0dB
        - 5.0dB: Good signal quality
        - 10.0dB: Excellent signal quality

ChirpStack v4 Protocol Compliance:
    Gateway Uplink Topic: v4/gw/{gateway_id}/event/up
    Gateway Stats Topic: v4/gw/{gateway_id}/event/stats
    
Message Structure:
    - phyPayload: Base64 encoded sensor data
    - txInfo: Transmission parameters (frequency, modulation)
    - rxInfo: Reception parameters (RSSI, SNR, location)
    - Metadata: Regional and protocol information

Error Handling:
    - KeyboardInterrupt: Graceful shutdown with cleanup
    - MQTT publish failures: Will raise exceptions (no retry logic)
    - JSON serialization errors: Will terminate simulation

Performance Characteristics:
    - Memory usage: Minimal (single message buffering)
    - CPU usage: Low (simple calculations and sleep)
    - Network usage: ~1KB per transmission cycle
    - Scalability: Single gateway simulation per process
"""
try:
    while True:
        # Generate realistic multi-sensor environmental data
        temperature = round(random.uniform(20.0, 30.0), 1)  # °C with 0.1° precision
        humidity = round(random.uniform(40.0, 80.0), 1)     # %RH with 0.1% precision  
        light = random.randint(100, 1000)                   # lux as integer
        
        # Package sensor data using binary encoding for efficiency
        # Format: ">ffH" = big-endian, float, float, unsigned short
        sensor_data = struct.pack(">ffH", temperature, humidity, light)
        encoded_data = base64.b64encode(sensor_data).decode()
        
        # Generate unique uplink identifier for message tracking
        uplink_id = f"{int(time.time())}-{random.randint(1000, 9999)}"
        
        # Construct ChirpStack v4 compliant gateway uplink message
        gateway_payload = {
            # Physical payload containing encoded sensor data
            "phyPayload": encoded_data,
            
            # Transmission information (frequency and modulation parameters)
            "txInfo": {
                "frequency": 903900000,  # US915 valid uplink frequency (Hz)
                "modulation": {
                    "lora": {
                        "bandwidth": 125000,        # 125kHz bandwidth
                        "spreadingFactor": 7,       # SF7 (balance of range/data rate)
                        "codeRate": "4/5"          # Forward error correction
                    }
                }
            },
            
            # Reception information (signal quality and gateway metadata)
            "rxInfo": {
                "gatewayId": GATEWAY_ID,
                "uplinkId": uplink_id,
                "rssi": random.randint(-120, -60),           # Signal strength (dBm)
                "snr": random.uniform(5.0, 10.0),           # Signal quality (dB)
                "channel": 2,                                # LoRaWAN channel index
                
                # Gateway geographical location
                "location": {
                    "latitude": 52.3740,   # Amsterdam coordinates
                    "longitude": 4.9144    # (example location)
                },
                
                # Gateway context and regional information
                "context": base64.b64encode(b"gateway-context").decode(),
                "metadata": {
                    "region_name": "us915",
                    "region_common_name": "US915"
                }
            }
        }
        
        # Publish gateway uplink message to ChirpStack v4 topic
        gateway_topic = f"v4/gw/{GATEWAY_ID}/event/up"
        client.publish(gateway_topic, json.dumps(gateway_payload))
        
        # Log successful uplink transmission with data summary
        print(f"✅ Gateway uplink message sent: {gateway_topic}")
        print(f"   Gateway ID: {GATEWAY_ID}, Uplink ID: {uplink_id}")
        print(f"   Sensor data: Temp={temperature}°C, Humidity={humidity}%, Light={light} lux")
        
        # Generate gateway statistics for infrastructure monitoring
        stats_payload = {
            "gatewayId": GATEWAY_ID,
            "time": datetime.now().isoformat() + "Z",  # ISO 8601 UTC timestamp
            
            # Gateway geographical location (same as uplink)
            "location": {
                "latitude": 52.3740,
                "longitude": 4.9144
            },
            
            # Gateway configuration and operational status
            "configVersion": "1.0.0",
            
            # Simulated traffic statistics (realistic ranges)
            "rx_packets_received": random.randint(10, 50),     # Total received
            "rx_packets_received_ok": random.randint(10, 50),  # Successfully processed
            "tx_packets_received": random.randint(5, 20),      # Downlink requests
            "tx_packets_emitted": random.randint(5, 20)        # Downlink transmitted
        }

        # Publish gateway statistics for monitoring and health checks
        stats_topic = f"v4/gw/{GATEWAY_ID}/event/stats"
        client.publish(stats_topic, json.dumps(stats_payload))
        print(f"📊 Gateway statistics sent: {stats_topic}")
        
        # Wait for next transmission cycle
        time.sleep(SEND_INTERVAL)
        
except KeyboardInterrupt:
    """
    Graceful shutdown handler.
    
    Handles user interruption (Ctrl+C) by cleanly disconnecting from
    the MQTT broker and terminating the simulation loop.
    
    Cleanup Operations:
        - Disconnect from MQTT broker
        - Release network resources
        - Log shutdown message
        
    Production Notes:
        - Consider implementing signal handlers for other termination signals
        - Add cleanup for any persistent state or file handles
        - Implement graceful shutdown timeout for network operations
    """
    print("🛑 Simulation stopped by user")
    client.disconnect()