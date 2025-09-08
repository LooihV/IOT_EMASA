"""
LoRaWAN Payload Processing Module

This module provides comprehensive processing capabilities for LoRaWAN device payloads
received via MQTT. It extracts, transforms, and structures IoT sensor data for
real-time consumption by Vue.js frontend applications.

Key Features:
- Complete LoRaWAN message parsing and extraction
- Binary data decoding (Base64 to hex)
- Radio frequency information processing
- Statistical analysis of measurement buffers
- Comprehensive error handling with detailed logging
- Frontend-optimized data structuring

Data Processing Pipeline:
    Raw MQTT Message -> JSON Decode -> Data Extraction -> 
    Statistical Analysis -> Frontend Structure -> WebSocket Ready

Supported Data Types:
    - Voltage measurements (continuous sampling buffers)
    - Current measurements (industrial monitoring)
    - Device telemetry and status information
    - Radio frequency parameters (RSSI, SNR, etc.)
    - Tenant and application metadata

Output Format:
    Structured dictionary optimized for Vue.js chart components
    with comprehensive device, radio, and measurement information.

Author: IoT Development Team
Version: 1.0
Date: July 2025
"""

import json
import base64
import logging
from datetime import datetime

def process_multi_sensor_data(object_data):
    """
    Process multi-sensor measurement data with multiple sensor types and channels.
    
    Args:
        object_data: Object containing measurements structure
        
    Returns:
        dict: Processed multi-sensor data structure
    """
    result = {
        "measurement_format": "multi_sensor",
        "active_sensors": object_data.get("active_sensors", []),
        "sensor_id": object_data.get("id"),
        "relative_timestamp": object_data.get("relative_timestamp"),
        "arrival_date": object_data.get("arrival_date"),
        "measurements": object_data["measurements"],
        "measurement_values": []
    }
    
    measurements = object_data["measurements"]
    
    # Process voltage measurements
    if "voltage" in measurements:
        voltage_data = measurements["voltage"]
        all_voltage_values = []
        
        for channel, samples in voltage_data.items():
            if isinstance(samples, list):
                all_voltage_values.extend([s.get("value", 0) for s in samples if "value" in s])
        
        if all_voltage_values:
            result["voltage_stats"] = {
                "total_samples": len(all_voltage_values),
                "min_voltage": min(all_voltage_values),
                "max_voltage": max(all_voltage_values),
                "avg_voltage": sum(all_voltage_values) / len(all_voltage_values),
                "channels": list(voltage_data.keys())
            }
    
    # Process current measurements
    if "current" in measurements:
        current_data = measurements["current"]
        all_current_values = []
        
        for channel, samples in current_data.items():
            if isinstance(samples, list):
                all_current_values.extend([s.get("value", 0) for s in samples if "value" in s])
        
        if all_current_values:
            result["current_stats"] = {
                "total_samples": len(all_current_values),
                "min_current": min(all_current_values),
                "max_current": max(all_current_values),
                "avg_current": sum(all_current_values) / len(all_current_values),
                "channels": list(current_data.keys())
            }
    
    # Create flattened measurement_values for compatibility
    for sensor_type, channels in measurements.items():
        for channel, samples in channels.items():
            if isinstance(samples, list):
                for sample in samples:
                    sample_copy = sample.copy()
                    sample_copy["sensor_type"] = sensor_type
                    sample_copy["channel"] = channel
                    result["measurement_values"].append(sample_copy)
    
    return result

def process_single_sensor_data(object_data):
    """
    Process single-sensor measurement data (legacy format).
    
    Args:
        object_data: Object containing values array
        
    Returns:
        dict: Processed single-sensor data structure
    """
    values = object_data["values"]
    
    result = {
        "measurement_format": "single_sensor",
        "measurement_values": values,
        "buffer_stats": {
            "total_samples": len(values),
            "sampling_period_seconds": 15,
            "sampling_interval_seconds": 0.3,
            "measurement_type": object_data.get("measurement", "Unknown"),
            "series_id": object_data.get("series_id"),
            "fragment_number": object_data.get("fragment_number"),
            "total_fragments": object_data.get("total_fragments"),
            "machine_uptime_ms": object_data.get("machine_uptime_ms"),
            "machine_start_time": object_data.get("machine_start_time")
        }
    }
    
    if values:
        # Análisis de los valores
        voltage_values = [v["value"] for v in values if "value" in v]
        if voltage_values:
            result["buffer_stats"].update({
                "min_voltage": min(voltage_values),
                "max_voltage": max(voltage_values),
                "avg_voltage": sum(voltage_values) / len(voltage_values),
                "first_sample_time": values[0].get("time_iso"),
                "last_sample_time": values[-1].get("time_iso")
            })
    
    return result

"""
Process LoRaWAN payload from MQTT message.

Comprehensive processor that extracts all relevant information from LoRaWAN
device messages, including device metadata, radio parameters, measurement
data, and statistical analysis for frontend consumption.

Processing Steps:
1. JSON payload decoding and validation
2. Device information extraction (tenant, application, device details)
3. Radio frequency parameter processing
4. Measurement buffer analysis and statistics
5. Binary data decoding (Base64 to hex)
6. Frontend-optimized data structuring

Args:
    msg: MQTT message object containing LoRaWAN payload
        - msg.payload: Raw binary payload (JSON encoded)
        - msg.topic: MQTT topic path
        
Returns:
    dict: Comprehensive data structure for frontend consumption containing:
        - Device Information: tenant, application, device profile details
        - Timing Data: message timestamps and reception time
        - Radio Parameters: RSSI, SNR, frequency, gateway information
        - Measurement Data: complete sampling buffer with statistics
        - Binary Data: decoded hex representation if available
        - Error Information: detailed error context for debugging
        
Data Structure Example:
    {
        "device_name": "VoltageMonitor_001",
        "measurement_values": [{"time_iso": "2025-07-31T10:30:00Z", "value": 12.5}, ...],
        "buffer_stats": {"total_samples": 50, "avg_voltage": 12.3, ...},
        "radio_info": {"rssi": -85, "snr": 8.5, "frequency": 915000000},
        ...
    }
    
Error Handling:
    - JSON decode errors: Returns error context with raw payload
    - Unicode errors: Provides binary data representation
    - Processing errors: Comprehensive error logging and context
    
Performance Notes:
    - Optimized for real-time processing of high-frequency data
    - Efficient memory usage for large measurement buffers
    - Statistical calculations performed in single pass
"""
def process_lorawan_payload(msg):
    try:
        # Decodificar JSON completo
        payload = msg.payload.decode()
        data = json.loads(payload)
        
        # EXTRAER TODA LA INFORMACIÓN IMPORTANTE
        frontend_data = {
            # TIEMPO
            "message_time": data.get("time"),
            "reception_timestamp": datetime.now().isoformat(),
            "topic": msg.topic,
            
            # INFORMACIÓN DEL TENANT Y APLICACIÓN
            "tenant_id": data.get("deviceInfo", {}).get("tenantId"),
            "tenant_name": data.get("deviceInfo", {}).get("tenantName"),
            "application_id": data.get("deviceInfo", {}).get("applicationId"),
            "application_name": data.get("deviceInfo", {}).get("applicationName"),
            
            # INFORMACIÓN DEL DISPOSITIVO
            "device_profile_id": data.get("deviceInfo", {}).get("deviceProfileId"),
            "device_profile_name": data.get("deviceInfo", {}).get("deviceProfileName"),
            "device_name": data.get("deviceInfo", {}).get("deviceName"),
            "dev_eui": data.get("deviceInfo", {}).get("devEui"),
            "dev_address": data.get("devAddr"),
            "dev_port": data.get("fPort"),  # fPort es el puerto del dispositivo
            
            # INFORMACIÓN DE LA TRAMA
            "frame_counter": data.get("fCnt"),
            "confirmed": data.get("confirmed"),
            "data_rate": data.get("dr"),
            "adr": data.get("adr"),
            
            # OBJETO COMPLETO (incluye todos los values del buffer)
            "object": data.get("object", {}),
            
            # TODOS LOS VALUES DEL BUFFER (15 segundos, cada 0.3s)
            "measurement_values": [],
            
            # INFORMACIÓN DE RADIO
            "radio_info": {
                "rssi": data.get("rxInfo", [{}])[0].get("rssi") if data.get("rxInfo") else None,
                "snr": data.get("rxInfo", [{}])[0].get("snr") if data.get("rxInfo") else None,
                "frequency": data.get("txInfo", {}).get("frequency"),
                "gateway_id": data.get("rxInfo", [{}])[0].get("gatewayId") if data.get("rxInfo") else None,
                "channel": data.get("rxInfo", [{}])[0].get("channel") if data.get("rxInfo") else None,
                "crc_status": data.get("rxInfo", [{}])[0].get("crcStatus") if data.get("rxInfo") else None
            },
            
            # DATOS BINARIOS SI EXISTEN
            "raw_data": data.get("data"),
            "raw_data_decoded": None
        }
        
        # Decodificar datos binarios si existen
        if "data" in data and data["data"]:
            try:
                raw_bytes = base64.b64decode(data["data"])
                frontend_data["raw_data_decoded"] = {
                    "hex": raw_bytes.hex(),
                    "length": len(raw_bytes)
                }
            except Exception as e:
                logging.warning(f"Error decodificando datos binarios: {e}")
        
        # DETECT FORMAT AND DELEGATE TO APPROPRIATE PROCESSOR
        object_data = data.get("object", {})
        
        if "measurements" in object_data:
            # NEW FORMAT: Multi-sensor with measurements structure
            frontend_data.update(process_multi_sensor_data(object_data))
        elif "values" in object_data:
            # OLD FORMAT: Single sensor with values array
            frontend_data.update(process_single_sensor_data(object_data))
        else:
            frontend_data["measurement_format"] = "unknown"
            logging.warning("No recognized measurement format found in object data")
        
        return frontend_data
        
    except json.JSONDecodeError as e:
        logging.error(f"Error decodificando JSON: {e}")
        return {
            "error": "json_decode_error",
            "topic": msg.topic,
            "raw_payload": msg.payload.decode() if msg.payload else None,
            "reception_timestamp": datetime.now().isoformat()
        }
    except UnicodeDecodeError as e:
        logging.error(f"Error decodificando UTF-8: {e}")
        return {
            "error": "unicode_decode_error", 
            "topic": msg.topic,
            "binary_data": {
                "hex": msg.payload.hex(),
                "length": len(msg.payload)
            },
            "reception_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logging.error(f"Error general procesando payload: {e}")
        return {
            "error": "processing_error",
            "error_message": str(e),
            "topic": msg.topic,
            "reception_timestamp": datetime.now().isoformat()
        }



"""
Log comprehensive processed data information.

Provides detailed console output of all extracted and processed LoRaWAN
data for monitoring, debugging, and system verification purposes.

Logging Categories:
1. Device Information: tenant, application, device profile details
2. Network Parameters: DevEUI, DevAddr, frame counters
3. Radio Frequency: RSSI, SNR, frequency, gateway information
4. Measurement Data: buffer statistics, voltage ranges, sampling info
5. Error Information: detailed error context and troubleshooting data

Args:
    frontend_data (dict): Processed payload data from process_lorawan_payload()
        Contains all extracted device, radio, and measurement information
        
Output Format:
    Structured console logging with emojis for visual clarity:
    📊 Device and application metadata
    📡 Radio frequency parameters
    📈 Measurement buffer analysis
    🔢 Statistical summaries
    📋 Sample data examples
    
Error Logging:
    Comprehensive error information for troubleshooting:
    - Error type and category
    - Raw payload data (if available)
    - Processing context and timestamps
    
Performance Impact:
    - Minimal overhead for production environments
    - Configurable logging levels
    - Optimized string formatting for high-frequency data
"""
def log_processed_data(frontend_data):
    """
    Muestra información procesada en los logs - Compatible con multi-sensor
    
    Args:
        frontend_data: Datos procesados del payload
    """
    if "error" in frontend_data:
        logging.error(f"❌ Error en payload: {frontend_data['error']}")
        return
    
    logging.info("📊 DATOS EXTRAÍDOS PARA FRONTEND:")
    logging.info(f"   🏢 Tenant: {frontend_data.get('tenant_name')} ({frontend_data.get('tenant_id')})")
    logging.info(f"   📱 App: {frontend_data.get('application_name')} ({frontend_data.get('application_id')})")
    logging.info(f"   🔧 Device Profile: {frontend_data.get('device_profile_name')} ({frontend_data.get('device_profile_id')})")
    logging.info(f"   📟 Device: {frontend_data.get('device_name')}")
    logging.info(f"   📡 DevEUI: {frontend_data.get('dev_eui')}")
    logging.info(f"   🏠 DevAddr: {frontend_data.get('dev_address')}")
    logging.info(f"   🚪 Port: {frontend_data.get('dev_port')}")
    logging.info(f"   ⏰ Tiempo: {frontend_data.get('message_time')}")
    logging.info(f"   📊 Frame: #{frontend_data.get('frame_counter')}")
    logging.info(f"   🔧 Format: {frontend_data.get('measurement_format', 'unknown')}")
    
    if frontend_data.get("radio_info"):
        radio = frontend_data["radio_info"]
        logging.info(f"   📡 Radio: RSSI={radio.get('rssi')}dBm, SNR={radio.get('snr')}dB")
    
    # Handle multi-sensor format
    if frontend_data.get('measurement_format') == 'multi_sensor':
        logging.info(f"   🌡️ Sensor ID: {frontend_data.get('sensor_id')}")
        logging.info(f"   📋 Active sensors: {', '.join(frontend_data.get('active_sensors', []))}")
        
        # Voltage measurements
        if frontend_data.get('voltage_stats'):
            v_stats = frontend_data['voltage_stats']
            logging.info(f"   ⚡ Voltage: {len(v_stats['channels'])} channels, {v_stats['total_samples']} samples")
            logging.info(f"      Range: {v_stats['min_voltage']:.1f}V - {v_stats['max_voltage']:.1f}V (avg: {v_stats['avg_voltage']:.2f}V)")
            logging.info(f"      Channels: {', '.join(v_stats['channels'])}")
        
        # Current measurements
        if frontend_data.get('current_stats'):
            c_stats = frontend_data['current_stats']
            logging.info(f"   🔌 Current: {len(c_stats['channels'])} channels, {c_stats['total_samples']} samples")
            logging.info(f"      Range: {c_stats['min_current']:.1f}A - {c_stats['max_current']:.1f}A (avg: {c_stats['avg_current']:.2f}A)")
            logging.info(f"      Channels: {', '.join(c_stats['channels'])}")
        
        # Show sample data
        if frontend_data.get("measurement_values"):
            values = frontend_data["measurement_values"]
            logging.info("   📋 Sample measurements:")
            for i, sample in enumerate(values[:3]):  # Show first 3 samples
                sensor_type = sample.get('sensor_type', 'unknown')
                channel = sample.get('channel', 'unknown')
                value = sample.get('value', 0)
                time_iso = sample.get('time', sample.get('time_iso', 'unknown'))
                logging.info(f"      [{i+1}] {sensor_type}.{channel}: {value} at {time_iso}")
    
    # Handle legacy single-sensor format
    elif frontend_data.get('measurement_format') == 'single_sensor':
        if frontend_data.get("measurement_values"):
            stats = frontend_data.get("buffer_stats", {})
            logging.info(f"   📈 Buffer: {stats.get('total_samples', 0)} muestras en {stats.get('sampling_period_seconds', 0)}s")
            if stats.get('avg_voltage') is not None:
                logging.info(f"   🔢 Voltaje: {stats.get('min_voltage', 0):.1f}V - {stats.get('max_voltage', 0):.1f}V (avg: {stats.get('avg_voltage', 0):.2f}V)")
            logging.info(f"   📊 Serie ID: {stats.get('series_id')}, Fragmento: {stats.get('fragment_number')}/{stats.get('total_fragments')}")
            
            # Mostrar algunos valores de ejemplo
            values = frontend_data["measurement_values"]
            logging.info("   📋 Primera muestra:")
            for i, sample in enumerate(values[:1]):
                logging.info(f"      [{i+1}] {sample.get('time_iso')} → {sample.get('value')}V")
    
    logging.info("=" * 80)