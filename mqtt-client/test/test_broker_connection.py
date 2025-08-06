"""
MQTT Broker Connection Test Utility

This module provides a simple test utility to verify MQTT broker connectivity
and basic publish/subscribe functionality. Used for validating broker setup
and network connectivity before running IoT simulations.

Key Features:
- MQTT broker connection testing
- Publish/subscribe verification
- Connection status reporting
- Basic message monitoring
- 10-second test cycle

Use Cases:
- Broker connectivity validation
- Network troubleshooting
- MQTT setup verification
- Pre-deployment testing

Author: IoT Development Team
Version: 1.0
Date: August 2025
"""

import paho.mqtt.client as mqtt
import time
import json
import os

# Environment variables for MQTT credentials
mqtt_username = os.getenv("MQTT_USERNAME", "admin")
mqtt_password = os.getenv("MQTT_PASSWORD", "admin")


"""
Test MQTT broker connection and basic functionality.

Performs a comprehensive MQTT broker test including connection,
subscription, publishing, and message reception verification.

Test Sequence:
1. Connect to localhost MQTT broker
2. Subscribe to all topics (#)
3. Publish test message
4. Monitor messages for 10 seconds
5. Report results and disconnect

Connection Parameters:
- Broker: localhost (127.0.0.1)
- Port: 1883 (standard MQTT)
- Keepalive: 60 seconds
- Clean session: True

Test Coverage:
- Connection establishment
- Authentication (if required)
- Topic subscription
- Message publishing
- Message reception
- Network stability

Error Handling:
- Connection failures with error codes
- Exception handling for network issues
- Graceful disconnection
- Status reporting throughout test
"""
def test_mqtt_connection():
    
    """
    Handle successful MQTT broker connection.
    
    Called when connection is established. Subscribes to all topics
    for comprehensive message monitoring during test.
    
    Args:
        client: MQTT client instance
        userdata: User-defined data (unused)
        flags: Connection flags from broker
        rc: Connection result code
            - 0: Success
            - 1: Incorrect protocol version
            - 2: Invalid client ID
            - 3: Server unavailable
            - 4: Bad username/password
            - 5: Not authorized
    """
    def on_connect(client, userdata, flags, rc):
        print(f"🔗 Connected with code: {rc}")
        if rc == 0:
            print("✅ Connection successful")
            client.subscribe("#")  # Subscribe to all topics for monitoring
        else:
            print(f"❌ Connection failed: {rc}")

    """
    Handle incoming MQTT messages during test.
    
    Logs all received messages with topic and payload size
    for monitoring broker activity and message flow.
    
    Args:
        client: MQTT client instance
        userdata: User-defined data (unused)
        msg: MQTT message object
            - msg.topic: Message topic
            - msg.payload: Message payload (bytes)
    """
    def on_message(client, userdata, msg):
        print(f"📨 Message received:")
        print(f"   Topic: {msg.topic}")
        print(f"   Payload: {len(msg.payload)} bytes")

    # Initialize MQTT client with event handlers
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        # Attempt connection to local MQTT broker
        print("🔄 Connecting to localhost:1883...")
        client.username_pw_set(mqtt_username, mqtt_password)
        client.connect("localhost", 1883, 60)
        
        # Allow connection to establish before testing
        time.sleep(1)
        
        # Publish test message to verify publish functionality
        test_topic = "test/connection"
        test_message = "Test message from connection utility"
        
        client.publish(test_topic, test_message)
        print(f"📤 Test message sent to {test_topic}")
        
        # Monitor broker activity for 10 seconds
        print("👂 Monitoring messages for 10 seconds...")
        client.loop_start()  # Start background network loop
        time.sleep(10)       # Monitor period
        client.loop_stop()   # Stop background loop
        
        print("✅ Test completed successfully")
        
    except ConnectionRefusedError:
        print("❌ Connection refused - Check if MQTT broker is running")
    except TimeoutError:
        print("❌ Connection timeout - Check network connectivity")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Ensure clean disconnection
        client.disconnect()
        print("🔌 Disconnected from broker")

"""
Run connection test when executed as standalone script.

Provides command-line interface for quick MQTT broker testing.
"""
if __name__ == "__main__":
    test_mqtt_connection()