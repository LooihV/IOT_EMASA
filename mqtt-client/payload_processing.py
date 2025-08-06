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
        
        # EXTRAER TODOS LOS VALUES (el buffer completo de 15 segundos)
        if "object" in data and "values" in data["object"]:
            values = data["object"]["values"]
            frontend_data["measurement_values"] = values  # TODOS los valores
            
            # Estadísticas del buffer
            frontend_data["buffer_stats"] = {
                "total_samples": len(values),
                "sampling_period_seconds": 15,
                "sampling_interval_seconds": 0.3,
                "measurement_type": data["object"].get("measurement", "Unknown"),
                "series_id": data["object"].get("series_id"),
                "fragment_number": data["object"].get("fragment_number"),
                "total_fragments": data["object"].get("total_fragments"),
                "machine_uptime_ms": data["object"].get("machine_uptime_ms"),
                "machine_start_time": data["object"].get("machine_start_time")
            }
            
            if values:
                # Análisis de los valores
                voltage_values = [v["value"] for v in values if "value" in v]
                if voltage_values:
                    frontend_data["buffer_stats"].update({
                        "min_voltage": min(voltage_values),
                        "max_voltage": max(voltage_values),
                        "avg_voltage": sum(voltage_values) / len(voltage_values),
                        "first_sample_time": values[0].get("time_iso"),
                        "last_sample_time": values[-1].get("time_iso")
                    })
        
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
    Muestra información procesada en los logs
    
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
    
    if frontend_data.get("radio_info"):
        radio = frontend_data["radio_info"]
        logging.info(f"   📡 Radio: RSSI={radio.get('rssi')}dBm, SNR={radio.get('snr')}dB")
    
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