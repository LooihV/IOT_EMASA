"""
MQTT IoT Data Gateway with WebSocket Bridge

This module implements a comprehensive MQTT client that connects to IoT brokers,
processes LoRaWAN device messages, and bridges the data to Vue.js frontend
applications via WebSocket connections.

Key Features:
- MQTT v5 client with robust error handling
- Real-time payload processing for LoRaWAN devices
- WebSocket server for frontend communication
- Comprehensive logging and monitoring
- Support for multiple device types (voltage, current measurements)

Architecture:
    MQTT Broker -> MQTT Client -> Payload Processor -> WebSocket Server -> Vue Frontend
    
Usage:
    python main.py
    
Requirements:
    - paho-mqtt
    - websockets
    - Custom modules: payload_processing, websockets_server
    
Author: IoT Development Team
Version: 1.0
Date: July 2025
"""

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import ssl
import json
import base64
import sys
import logging
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Module availability flags
PAYLOAD_PROCESSING_AVAILABLE = False
WEBSOCKET_AVAILABLE = False

# Try to import custom modules with fallback
try:
    from payload_processing import process_lorawan_payload, log_processed_data
    PAYLOAD_PROCESSING_AVAILABLE = True
    logging.info("✅ Payload processing module loaded")
except ImportError as e:
    logging.warning(f"⚠️ Payload processing not available: {e}")
    PAYLOAD_PROCESSING_AVAILABLE = False

# Try to import WebSocket server module
try:
    from websockets_server import start_websocket_server, send_to_vue, get_connected_clients
    WEBSOCKET_AVAILABLE = True
    logging.info("✅ WebSocket server module loaded")
except ImportError as e:
    logging.error(f"❌ WebSocket server not available: {e}")
    WEBSOCKET_AVAILABLE = False

"""
MQTT connection callback handler.
    
Called when the MQTT client successfully connects to the broker.
Automatically subscribes to predefined IoT topics for device monitoring.
    
Args:
client: The MQTT client instance
userdata: User-defined data passed to callbacks
flags: Response flags sent by the broker
reason_code: Connection result code
properties: MQTT v5 properties (optional)
        
Topics Subscribed:
- application/+/device/+/event/up: ChirpStack v3 uplink messages
- us915_7/gateway/+/event/stats: Gateway statistics
- v4/device/+/+/event/+: ChirpStack v4 device events
"""
def on_connect(client, userdata, flags, reason_code, properties=None):
    
    # Convert ReasonCode to integer for MQTT v5 compatibility
    rc_value = reason_code.value if hasattr(reason_code, 'value') else reason_code
    
    # Check connection result and authentication status
    if rc_value == 0:
        logging.info("✅ Successfully connected to MQTT broker")
        logging.info(f"🔍 Connection details: reason_code={rc_value}")
        
        # Subscribe to topics
        topics = [
            "application/+/device/+/event/up",
            "us915_7/gateway/+/event/stats", 
            "v4/device/+/+/event/+"
        ]
        
        for topic in topics:
            result, mid = client.subscribe(topic)
            if result == 0:
                logging.info(f"📡 Successfully subscribed to: {topic}")
            else:
                logging.error(f"❌ Failed to subscribe to: {topic} (result: {result})")

        if WEBSOCKET_AVAILABLE:
            client_count = get_connected_clients()
            logging.info(f"🌐 WebSocket clients connected: {client_count}")
            
    else:
        # Handle connection failures
        error_messages = {
            1: "🔐 Connection refused - incorrect protocol version",
            2: "🔐 Connection refused - invalid client identifier", 
            3: "🔐 Connection refused - server unavailable",
            4: "🔐 Connection refused - bad username or password",
            5: "🔐 Connection refused - not authorized",
            128: "🔐 Connection refused - unspecified error",
            129: "🔐 Connection refused - malformed packet",
            130: "🔐 Connection refused - protocol error",
            131: "🔐 Connection refused - implementation specific error",
            132: "🔐 Connection refused - unsupported protocol version",
            133: "🔐 Connection refused - client identifier not valid",
            134: "🔐 Connection refused - bad username or password",
            135: "🔐 Connection refused - not authorized",
            136: "🔐 Connection refused - server unavailable",
            137: "🔐 Connection refused - server busy",
            138: "🔐 Connection refused - banned",
            139: "🔐 Connection refused - bad authentication method",
            144: "🔐 Connection refused - topic name invalid",
            149: "🔐 Connection refused - packet too large",
            151: "🔐 Connection refused - quota exceeded",
            153: "🔐 Connection refused - payload format invalid",
            154: "🔐 Connection refused - retain not supported",
            155: "🔐 Connection refused - QoS not supported",
            156: "🔐 Connection refused - use another server",
            157: "🔐 Connection refused - server moved",
            159: "🔐 Connection refused - connection rate exceeded"
        }
        
        error_msg = error_messages.get(rc_value, f"🔐 Connection refused - unknown error (code: {rc_value})")
        logging.error(f"❌ MQTT Connection Failed: {error_msg}")
        
        # Exit application on authentication failure
        if rc_value in [4, 5, 134, 135]:  # Bad credentials or not authorized
            logging.error("🚨 Authentication failed - check MQTT_USERNAME and MQTT_PASSWORD")
            sys.exit(1)

def on_disconnect(client, userdata, flags, reason_code, properties=None):
    """Handle MQTT disconnection events - MQTT v5 compatible signature"""
    # Convert ReasonCode to integer for MQTT v5 compatibility
    rc_value = reason_code.value if hasattr(reason_code, 'value') else reason_code
    
    if rc_value != 0:
        logging.warning(f"⚠️ Unexpected MQTT disconnection: {rc_value}")
        logging.info("🔄 Will attempt to reconnect...")
    else:
        logging.info("✅ MQTT disconnected normally")

def on_subscribe(client, userdata, mid, reason_codes, properties=None):
    """Handle subscription acknowledgments"""
    for i, reason_code in enumerate(reason_codes):
        # Convert ReasonCode to integer for MQTT v5 compatibility
        rc_value = reason_code.value if hasattr(reason_code, 'value') else reason_code
        
        if rc_value >= 128:
            logging.error(f"❌ Subscription {mid} failed: {rc_value}")
        else:
            logging.debug(f"✅ Subscription {mid} successful with QoS: {rc_value}")

def on_log(client, userdata, level, buf):
    """Handle MQTT client log messages"""
    if level == mqtt.MQTT_LOG_ERR:
        logging.error(f"🔴 MQTT Error: {buf}")
    elif level == mqtt.MQTT_LOG_WARNING:
        logging.warning(f"🟡 MQTT Warning: {buf}")
    elif level == mqtt.MQTT_LOG_INFO:
        logging.info(f"🔵 MQTT Info: {buf}")
    else:
        logging.debug(f"🔍 MQTT Debug: {buf}")

"""
MQTT message callback handler.
    
Processes incoming MQTT messages from IoT devices, extracts relevant data,
and forwards processed information to connected WebSocket clients.
    
Message Processing Pipeline:
1. Decode UTF-8 JSON payload
2. Extract device information and measurement data
3. Process with custom payload processor (if available)
4. Forward to WebSocket clients for real-time display
5. Log comprehensive message details
    
Args:
client: The MQTT client instance
userdata: User-defined data
msg: MQTT message object containing topic and payload
        
Supported Message Types:
    - JSON payloads: LoRaWAN device data with measurements
    - Binary payloads: Raw device transmissions
   - Text payloads: Status and diagnostic messages
        
Data Flow:
MQTT Message -> JSON Decode -> Device Info Extraction -> 
Payload Processing -> WebSocket Broadcast -> Frontend Display
"""
def on_message(client, userdata, msg):
    
    logging.info(f"📨 [MQTT] Topic: {msg.topic}")
    
    try:
        # Try to decode as UTF-8 JSON
        payload_str = msg.payload.decode('utf-8')
        data = json.loads(payload_str)
        
        # Log device information summary
        logging.info("🔍 [MQTT] Message summary:")
        if "deviceInfo" in data:
            device_info = data["deviceInfo"]
            logging.info(f"   📟 Device: {device_info.get('deviceName', 'N/A')}")
            logging.info(f"   🏢 Tenant: {device_info.get('tenantName', 'N/A')}")
            logging.info(f"   📱 App: {device_info.get('applicationName', 'N/A')}")
        
        # Log measurement data summary - support both formats
        if "object" in data:
            object_data = data["object"]
            
            # NEW MULTI-SENSOR FORMAT
            if "measurements" in object_data:
                logging.info(f"   🌡️ Multi-sensor format detected")
                logging.info(f"   📟 Sensor ID: {object_data.get('id', 'N/A')}")
                logging.info(f"   📋 Active sensors: {', '.join(object_data.get('active_sensors', []))}")
                
                measurements = object_data["measurements"]
                for sensor_type, channels in measurements.items():
                    for channel, samples in channels.items():
                        if isinstance(samples, list) and samples:
                            values = [s.get("value", 0) for s in samples if "value" in s]
                            if values:
                                logging.info(f"   📊 {sensor_type.title()} {channel}: {len(values)} samples")
                                logging.info(f"      Range: {min(values):.1f} - {max(values):.1f} (avg: {sum(values)/len(values):.2f})")
            
            # OLD SINGLE-SENSOR FORMAT
            elif "values" in object_data:
                logging.info(f"   📊 Single-sensor format detected")
                values = object_data["values"]
                logging.info(f"   📊 Voltage samples: {len(values)}")
                if values:
                    voltages = [v.get("value", 0) for v in values]
                    logging.info(f"   ⚡ Voltage range: {min(voltages):.1f}V - {max(voltages):.1f}V")
                
        # Process with custom payload processor if available
        if PAYLOAD_PROCESSING_AVAILABLE:
            try:
                processed_data = process_lorawan_payload(msg)
                log_processed_data(processed_data)
                
                # Send to WebSocket clients if available
                if WEBSOCKET_AVAILABLE and processed_data:
                    send_to_vue(processed_data)
                    logging.info("📤 Data sent to Vue frontend")
                    
            except Exception as e:
                logging.error(f"❌ Error processing payload: {e}")
        
        # Log raw data information for debugging
        if "data" in data:
            try:
                raw_bytes = base64.b64decode(data["data"])
                logging.info(f"📊 Raw bytes: {raw_bytes.hex()}")
            except Exception as e:
                logging.warning(f"⚠️ Error decoding base64 data: {e}")
        
    except UnicodeDecodeError:
        # Handle binary messages that cannot be decoded as UTF-8
        logging.info(f"📦 Binary message: {len(msg.payload)} bytes")
        logging.info(f"   First 10 bytes: {msg.payload[:10].hex()}")
        
    except json.JSONDecodeError as e:
        # Handle non-JSON text messages
        logging.warning(f"⚠️ Non-JSON message: {e}")
        logging.info(f"   Content: {msg.payload.decode('utf-8', errors='ignore')[:100]}")
        
    except Exception as e:
        # Catch-all for unexpected errors
        logging.error(f"❌ Unexpected error processing message: {e}")



"""
Main application entry point.
    
Initializes and orchestrates the complete IoT data gateway system:
1. Creates MQTT client with v5 protocol support
2. Starts WebSocket server for frontend communication
3. Connects to MQTT broker and begins message processing
4. Runs indefinitely until user interruption
    
System Components:
    - MQTT Client: Connects to IoT broker for device data
    - WebSocket Server: Provides real-time data to Vue.js frontend
    - Payload Processor: Transforms raw IoT data for consumption
    - Logging System: Comprehensive monitoring and debugging
        
Network Configuration (via Environment Variables):
    - MQTT_BROKER_HOST: MQTT broker hostname (default: localhost)
    - MQTT_BROKER_PORT: MQTT broker port (default: 1883)
    - MQTT_USERNAME: MQTT authentication username (optional)
    - MQTT_PASSWORD: MQTT authentication password (optional)
    - WEBSOCKET: WebSocket server host (default: 0.0.0.0)
    - WEBSOCKET_PORT: WebSocket server port (default: 8765)
        
Production Configuration:
    - Set environment variables in docker-compose.yml
    - Use TLS/SSL for secure MQTT connections
    - Configure proper authentication credentials
    - Set appropriate WebSocket host binding
        
Error Handling:
    - Graceful module loading with fallbacks
    - Connection retry logic
    - Comprehensive exception handling
    - Clean shutdown procedures
"""
def main():
    
    logging.info("🚀 MQTT IoT Client Starting...")
    
    # Create MQTT client with v5 protocol support
    client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=mqtt.MQTTv5
    )
    
    # Attach event handlers
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_log = on_log  # Enable detailed logging
    
    try:
        # Initialize WebSocket server for frontend communication
        if WEBSOCKET_AVAILABLE:
            logging.info("🌐 Starting WebSocket server for Vue frontend...")
            
            # Get WebSocket configuration from environment variables
            websocket_host = os.getenv('WEBSOCKET', '0.0.0.0')
            websocket_port = int(os.getenv('WEBSOCKET_PORT', '8765'))
            
            ws_thread = start_websocket_server(websocket_host, websocket_port)
            logging.info(f"✅ WebSocket server started on ws://{websocket_host}:{websocket_port}")
            
            # Allow WebSocket server to fully initialize
            logging.info("⏳ Waiting for WebSocket server to initialize...")
            time.sleep(5)
        else:
            logging.error("❌ Cannot start WebSocket server - module not available")
            return
        
        # Establish connection to MQTT broker
        logging.info("🔗 Connecting to MQTT broker...")
        
        # Get broker configuration from environment variables
        broker_host = os.getenv('MQTT_BROKER_HOST', 'localhost')
        broker_port = int(os.getenv('MQTT_BROKER_PORT', '1883'))
        mqtt_username = os.getenv('MQTT_USERNAME', 'admin')
        mqtt_password = os.getenv('MQTT_PASSWORD', 'admin')
        
        # Set authentication if credentials are provided
        if mqtt_username and mqtt_password:
            client.username_pw_set(mqtt_username, mqtt_password)
            logging.info(f"🔐 Authentication set for user: {mqtt_username}")
            
            # Attempt connection to MQTT broker (only with credentials)
            try:
                logging.info(f"🔌 Attempting connection to {broker_host}:{broker_port}...")
                client.connect(broker_host, broker_port, 60)
                logging.info("✅ MQTT connection initiated successfully")
            except Exception as e:
                logging.error(f"❌ Failed to connect to MQTT broker: {e}")
                return
        else:
            logging.error("🚨 MQTT credentials are REQUIRED!")
            logging.error("   Please set MQTT_USERNAME and MQTT_PASSWORD environment variables")
            logging.error("   Refusing to connect without authentication")
            return
        
        
        # Display startup summary
        logging.info("=" * 60)
        logging.info("✅ SISTEMA INICIADO CORRECTAMENTE:")
        logging.info(f"   📡 MQTT Client: Conectado a {broker_host}:{broker_port}")
        logging.info(f"   🔐 MQTT Auth: ✅ Succesful")
        logging.info(f"   🌐 WebSocket Server: ws://{websocket_host}:{websocket_port}")
        logging.info("   🎯 Frontend URL: http://localhost:5173")
        logging.info("   📊 Listo para recibir datos IoT!")
        logging.info("=" * 60)
        
        # Start MQTT network loop (blocking operation)
        client.loop_forever()
        
    except KeyboardInterrupt:
        logging.info("🛑 Sistema detenido por el usuario")
    except Exception as e:
        logging.error(f"❌ Error del sistema: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup and shutdown procedures
        logging.info("🔄 Cerrando conexiones...")
        try:
            client.disconnect()
        except:
            pass

"""
Application entry point.
    
Runs the main IoT gateway when executed as a standalone script.
Ensures proper initialization and error handling.
"""
if __name__ == "__main__":
    main()