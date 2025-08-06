"""
Docker Health Check for MQTT Service

Lightweight health check specifically designed for Docker container monitoring.
Fast execution with minimal resource overhead for container orchestration.

Usage in Dockerfile:
    HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
        CMD python health_check.py --docker || exit 1

Author: IoT Development Team
Version: 1.0
Date: August 2025
"""

import paho.mqtt.client as mqtt
import sys
import time
import json
import os

def docker_health_check(timeout=5):
    """
    Lightweight health check for Docker containers.
    
    Tests essential MQTT connectivity with minimal overhead.
    Returns exit code 0 for healthy, 1 for unhealthy.
    
    Args:
        timeout: Connection timeout in seconds
        
    Returns:
        dict: Basic health status for logging
    """
    health_status = {
        "timestamp": time.time(),
        "status": "unknown",
        "message": "",
        "response_time_ms": 0
    }
    
    start_time = time.time()
    
    try:
        # Get MQTT broker settings from environment or defaults
        broker_host = os.getenv('MQTT_BROKER', 'localhost')
        broker_port = int(os.getenv('MQTT_PORT', '1883'))
        
        # Quick connection test
        client = mqtt.Client()
        client.connect(broker_host, broker_port, timeout)
        
        # Test basic publish capability
        client.publish("health/check", "docker_health_ping")
        client.disconnect()
        
        response_time = int((time.time() - start_time) * 1000)
        
        health_status.update({
            "status": "healthy",
            "message": f"MQTT broker responsive in {response_time}ms",
            "response_time_ms": response_time
        })
        
        return health_status
        
    except Exception as e:
        health_status.update({
            "status": "unhealthy", 
            "message": f"MQTT connection failed: {str(e)}",
            "response_time_ms": -1
        })
        
        return health_status

def docker_websocket_health_check():
    """
    Quick WebSocket server health check for Docker.
    
    Returns:
        dict: WebSocket health status
    """
    try:
        # Only check if the module is importable
        from websockets_server import get_connected_clients
        client_count = get_connected_clients()
        
        return {
            "status": "healthy",
            "message": f"WebSocket server running ({client_count} clients)",
            "client_count": client_count
        }
    except ImportError:
        return {
            "status": "degraded",
            "message": "WebSocket module not available"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"WebSocket error: {str(e)}"
        }

def main():
    """
    Main health check execution for Docker.
    
    Supports different modes based on command line arguments:
    - --docker: Lightweight Docker health check
    - --detailed: Comprehensive health check
    - (no args): Standard health check
    """
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if "--docker" in sys.argv:
            # Docker health check mode
            health = docker_health_check()
            
            # Log health status
            print(json.dumps(health))
            
            # Exit with appropriate code for Docker
            if health["status"] == "healthy":
                sys.exit(0)  # Healthy
            else:
                sys.exit(1)  # Unhealthy
                
        elif "--detailed" in sys.argv:
            # Detailed health check (use the comprehensive version)
            from health_check_detailed import health_checker
            health = health_checker.comprehensive_health_check()
            print(json.dumps(health, indent=2))
            sys.exit(0)
    
    # Standard health check mode
    mqtt_health = docker_health_check()
    ws_health = docker_websocket_health_check()
    
    overall_status = "healthy"
    if mqtt_health["status"] != "healthy" or ws_health["status"] == "unhealthy":
        overall_status = "unhealthy"
    elif ws_health["status"] == "degraded":
        overall_status = "degraded"
    
    health_report = {
        "timestamp": time.time(),
        "overall_status": overall_status,
        "mqtt_broker": mqtt_health,
        "websocket_server": ws_health
    }
    
    print(json.dumps(health_report, indent=2))
    
    # Exit code for automated monitoring
    if overall_status == "healthy":
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()