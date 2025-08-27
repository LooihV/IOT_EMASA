"""
ChirpStack v4 Connection Test

This script tests different ChirpStack v4 Basic Station endpoints
to find the correct one for your setup.
"""

import asyncio
import websockets
import json
import logging

# Test configurations
CHIRPSTACK_HOST = "localhost"
GATEWAY_EUI = "a0102030a4b0c5d1"

# Common ChirpStack v4 endpoints to test
ENDPOINTS = [
    f"ws://{CHIRPSTACK_HOST}:8080/api/gateways/{GATEWAY_EUI}/connection/websocket",
    f"ws://{CHIRPSTACK_HOST}:8080/gateway/{GATEWAY_EUI}",
    f"ws://{CHIRPSTACK_HOST}:3001/gateway/{GATEWAY_EUI}",
    f"ws://{CHIRPSTACK_HOST}/api/gateways/{GATEWAY_EUI}/connection/websocket",
    f"ws://{CHIRPSTACK_HOST}/gateway/{GATEWAY_EUI}",
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_endpoint(uri):
    """Test a specific endpoint"""
    try:
        logger.info(f"Testing: {uri}")
        websocket = await websockets.connect(uri, ping_timeout=5, ping_interval=None)
        logger.info(f"✅ SUCCESS: Connected to {uri}")
        
        # Try sending a version message
        version_msg = {
            "msgtype": "version",
            "station": "Test Station",
            "firmware": "1.0.0",
            "package": "test"
        }
        
        await websocket.send(json.dumps(version_msg))
        logger.info(f"   Sent version message")
        
        # Wait for response (with timeout)
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            logger.info(f"   Received: {response}")
        except asyncio.TimeoutError:
            logger.info(f"   No response received (timeout)")
        
        await websocket.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ FAILED: {uri} - {e}")
        return False

async def main():
    print("🔍 Testing ChirpStack v4 Basic Station Endpoints")
    print(f"   Gateway EUI: {GATEWAY_EUI}")
    print(f"   Host: {CHIRPSTACK_HOST}")
    print("\n" + "="*60)
    
    success_count = 0
    for endpoint in ENDPOINTS:
        if await test_endpoint(endpoint):
            success_count += 1
        print()
    
    print("="*60)
    if success_count > 0:
        print(f"✅ Found {success_count} working endpoint(s)")
        print("   Update the CHIRPSTACK_SERVER in the main simulator")
    else:
        print("❌ No working endpoints found")
        print("   Check:")
        print("   - ChirpStack is running")
        print("   - Gateway is registered with EUI: a0102030a4b0c5d1")
        print("   - Basic Station is enabled")
        print("   - Port 8080 is accessible")

if __name__ == "__main__":
    asyncio.run(main())
