# MQTT IoT Data Gateway Documentation

## Overview

The MQTT IoT Data Gateway is a comprehensive system that bridges IoT device data from MQTT brokers to web-based dashboards. It processes LoRaWAN device messages in real-time and provides a WebSocket interface for frontend applications.

## Architecture
![Diagram](resources/SVG/MQTT_Client_workflow_diagram.svg)


## Module Structure

### main.py
**Primary Components:**

1. **MQTT Client** (`paho-mqtt`)
   - Connects to IoT broker using MQTT v5 protocol
   - Subscribes to device uplink topics
   - Handles connection management and reconnection

2. **WebSocket Server** (`websockets_server.py`)
   - Provides real-time data streaming to frontend
   - Manages multiple client connections
   - Broadcasts processed IoT data

3. **Payload Processor** (`payload_processing.py`)
   - Transforms raw LoRaWAN payloads
   - Extracts measurement values
   - Formats data for frontend consumption

## Configuration

### BASIC Network Settings
```python
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8765
```



## Data Flow

### 1. Device Message Reception
```python
def on_message(client, userdata, msg):
    # Decode UTF-8 JSON payload
    # Extract device information
    # Process measurement data
    # Forward to WebSocket clients
```

### 2. Payload Processing Pipeline
1. **Raw MQTT Message** → JSON Decode
2. **Device Info Extraction** → Device name, tenant, application
3. **Measurement Processing** → Voltage/current values with timestamps
4. **WebSocket Broadcast** → Real-time frontend updates

### 3. Error Handling
- **Connection Failures**: Automatic reconnection with exponential backoff
- **Malformed Data**: Graceful handling of non-JSON and binary messages
- **Module Dependencies**: Fallback operation when optional modules unavailable

## Message Format

### Input (MQTT)
```json
"object": {
    "type": "voltage",
    "values": [
      {
        "time": 1690804800000,
        "time_iso": "2023-07-31T12:00:00.000Z",
        "value": 3.7
      }
    ]
 }

```

### Output (WebSocket)
```json
{
  "object": {
    "type": "voltage",
    "values": [...]
  }
}
```

## Dependencies

### Required Packages
```bash
pip install -r requirements.txt
```

### Custom Modules
- `payload_processing.py` - LoRaWAN payload transformation
- `websockets_server.py` - WebSocket server implementation

## Usage

### Basic Startup
```bash
python main.py
```

### Development Mode
```bash
# Terminal 1: Start backend
python main.py

# Terminal 2: Test with Mosquitto MQTT Broker
python test_broker_connection.py

#Terminal 3: Send test gateway evets
python gateway_simulator.py

#Terminal 3: Send current test data
python current_simulator.py

#Terminal 3: Send voltage test data
python voltage_simulator.py

# Terminal 2: Send dual (current and voltage) test data
python dual_simulator.py
```

## Logging

The system provides comprehensive logging with different levels:

- **INFO**: Normal operation events
- **WARNING**: Non-critical issues
- **ERROR**: Critical failures requiring attention

### Log Format
```
2023-07-31 12:00:00,000 - root - INFO - ✅ Connected with result code: 0
2023-07-31 12:00:01,000 - root - INFO - 📨 [MQTT] Topic: v4/device/app/device123/event/up
2023-07-31 12:00:02,000 - root - INFO - 📤 Data sent to Vue frontend
```

## Performance Considerations

### Memory Usage
- Message buffering limited to recent 10 messages per device
- WebSocket client management with automatic cleanup

### Network Optimization
- Efficient JSON parsing and data transformation
- Minimal payload processing overhead
- Optimized WebSocket broadcasting

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   ```bash
   ❌ WebSocket server not available: No module named 'websockets_server'
   ```
   **Solution**: Ensure `websockets_server.py` is in the module path

2. **MQTT Connection Timeout**
   ```bash
   ❌ Error del sistema: [Errno 10060] Connection timed out
   ```
   **Solution**: Verify broker IP address and network connectivity

3. **Payload Processing Errors**
   ```bash
   ❌ Error processing payload: 'object' key not found
   ```
   **Solution**: Check message format compatibility

## Security Considerations

- **Network Security**: Consider TLS encryption for production deployments
- **Access Control**: Implement authentication for WebSocket connections
- **Data Validation**: Sanitize and validate all incoming MQTT messages

## Monitoring and Maintenance

### Health Checks
- Monitor MQTT connection status
- Track WebSocket client count
- Verify payload processing rates

### Performance Metrics
- Message processing latency
- WebSocket broadcast efficiency
- Memory usage patterns

## Version History

- **v2.0** (July 2025): Initial release with full MQTT-WebSocket bridge functionality
- Support for voltage and current measurements
- Vue.js frontend integration
- Comprehensive error handling and logging
