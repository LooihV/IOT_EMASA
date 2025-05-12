import os
import sys
import paho.mqtt.client as mqtt
import time
import psutil

# Configuration - use the same environment variables as your main app
"""MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST", "mqtt-broker")
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT", 1883))
MAIN_PROCESS_NAME = "main.py"  # Adjust if your main script has a different name
"""
MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST")
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT"))
MAIN_PROCESS_NAME = "main.py"  # Adjust if your main script has a different name

def is_main_process_running():
    """Check if the main process is running"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if this is our main python process
            if proc.info['name'] == 'python' and any(MAIN_PROCESS_NAME in cmd for cmd in proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def can_connect_to_broker():
    """Test if we can connect to the MQTT broker"""
    client = mqtt.Client(client_id="health-check")
    client.connect_status = False
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.connect_status = True
        client.disconnect()
    
    client.on_connect = on_connect
    
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 5)
        client.loop_start()
        # Give it time to attempt connection
        time.sleep(3)
        client.loop_stop()
        return client.connect_status
    except Exception:
        return False

def main():
    """Run health checks and exit with appropriate code"""
    # Check 1: Is main process running?
    if not is_main_process_running():
        print("Main process is not running")
        sys.exit(1)
    
    # Check 2: Can we connect to the MQTT broker?
    if not can_connect_to_broker():
        print("Cannot connect to MQTT broker")
        sys.exit(1)
    
    # All checks passed
    print("Health check passed")
    sys.exit(0)

if __name__ == "__main__":
    main()