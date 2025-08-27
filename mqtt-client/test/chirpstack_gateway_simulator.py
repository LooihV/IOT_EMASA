"""
ChirpStack Gateway Simulator using Basic Station Protocol

This simulator implements the LoRa Basic Station protocol over WebSockets
to connect to ChirpStack as a real gateway. It will appear as "online"
in the ChirpStack gateway management interface.

Features:
- Basic Station protocol implementation
- WebSocket connection to ChirpStack
- Gateway status reporting (appears as online)
- Uplink message simulation
- Downlink message handling
- Automatic reconnection on connection loss

Requirements:
- websockets library: pip install websockets
- ChirpStack server with Basic Station enabled

Configuration:
- Update CHIRPSTACK_SERVER and GATEWAY_EUI for your setup
- Gateway must be registered in ChirpStack with matching EUI
"""

import asyncio
import websockets
import json
import base64
import time
import random
import struct
from datetime import datetime, timezone
import logging

# Configuration
CHIRPSTACK_SERVER = "localhost:3001"  # ChirpStack v4 Basic Station endpoint (found working)
GATEWAY_EUI = "a0102030a4b0c5d1"     # Must match registered gateway in ChirpStack
GATEWAY_ID = GATEWAY_EUI

# Basic Station protocol message types
MSG_VERSION = "version"
MSG_ROUTER_INFO = "router_info"
MSG_UPLINK = "updf"
MSG_DOWNLINK = "dndf"
MSG_TIMESYNC = "timesync"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChirpStackGatewaySimulator:
    def __init__(self):
        self.websocket = None
        self.gateway_eui = GATEWAY_EUI
        self.running = False
        
    async def connect(self):
        """Connect to ChirpStack using Basic Station protocol"""
        # Use the working endpoint found by our test
        uri = f"ws://{CHIRPSTACK_SERVER}/gateway/{self.gateway_eui}"
        
        try:
            self.websocket = await websockets.connect(uri)
            logger.info(f"Connected to ChirpStack v4: {uri}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False
    
    async def send_version(self):
        """Send version information to establish connection"""
        version_msg = {
            "msgtype": MSG_VERSION,
            "station": "ChirpStack Gateway Simulator",
            "firmware": "1.0.0",
            "package": "simulator",
            "model": "SIM-001",
            "protocol": 2,
            "features": "gps rmtsh"
        }
        
        await self.websocket.send(json.dumps(version_msg))
        logger.info("Sent version message")
    
    async def send_router_info(self):
        """Send router info to complete handshake"""
        router_info = {
            "msgtype": MSG_ROUTER_INFO,
            "router": f"{CHIRPSTACK_SERVER.split(':')[0]}:1700",
            "muxs": f"{CHIRPSTACK_SERVER.split(':')[0]}:1700"
        }
        
        await self.websocket.send(json.dumps(router_info))
        logger.info("Sent router info")
    
    async def send_uplink(self):
        """Send simulated uplink message"""
        # Generate sensor data (temp, humidity, light)
        temperature = round(random.uniform(20.0, 30.0), 1)
        humidity = round(random.uniform(40.0, 80.0), 1)
        light = random.randint(100, 1000)
        
        # Pack sensor data
        sensor_data = struct.pack(">ffH", temperature, humidity, light)
        phy_payload = base64.b64encode(sensor_data).decode()
        
        # Current time in GPS microseconds (Basic Station format)
        gps_time = int(time.time() * 1000000)
        
        uplink_msg = {
            "msgtype": MSG_UPLINK,
            "rxpk": [{
                "time": datetime.now(timezone.utc).isoformat(),
                "tmms": gps_time,
                "tmst": int(time.time() * 1000000) % (2**32),  # 32-bit timestamp
                "freq": 903.9,  # US915_7 frequency in MHz
                "chan": 0,
                "rfch": 0,
                "stat": 1,
                "modu": "LORA",
                "datr": "SF7BW125",  # Spreading factor and bandwidth (US915)
                "codr": "4/5",        # Coding rate
                "rssi": random.randint(-120, -60),
                "lsnr": round(random.uniform(5.0, 10.0), 1),
                "size": len(sensor_data),
                "data": phy_payload,
                # GPS coordinates (optional)
                "lati": 40.7128,
                "long": -74.0060,
                "alti": 10
            }]
        }
        
        await self.websocket.send(json.dumps(uplink_msg))
        logger.info(f"Sent uplink: Temp={temperature}°C, Humidity={humidity}%, Light={light}lux")
    
    async def handle_downlink(self, message):
        """Handle downlink messages from ChirpStack"""
        try:
            data = json.loads(message)
            if data.get("msgtype") == MSG_DOWNLINK:
                logger.info("Received downlink message")
                # In a real gateway, this would be transmitted to the device
                # For simulation, we just acknowledge receipt
                
                # Send TX acknowledgment
                tx_ack = {
                    "msgtype": "dntxed",
                    "diid": data.get("dnpk", {}).get("diid", 0)
                }
                await self.websocket.send(json.dumps(tx_ack))
                logger.info("Sent TX acknowledgment")
                
        except Exception as e:
            logger.error(f"Error handling downlink: {e}")
    
    async def message_handler(self):
        """Handle incoming messages from ChirpStack"""
        try:
            async for message in self.websocket:
                await self.handle_downlink(message)
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed")
        except Exception as e:
            logger.error(f"Message handler error: {e}")
    
    async def send_stats(self):
        """Send gateway statistics to show as online"""
        stats_msg = {
            "msgtype": "stat",
            "stat": {
                "time": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S GMT'),
                "lati": 40.7128,  # Latitude
                "long": -74.0060, # Longitude
                "alti": 10,       # Altitude
                "rxnb": random.randint(10, 50),    # Number of radio packets received
                "rxok": random.randint(10, 50),    # Number of radio packets received with valid CRC
                "rxfw": random.randint(5, 25),     # Number of radio packets forwarded
                "ackr": random.uniform(95.0, 100.0), # Percentage of upstream datagrams acknowledged
                "dwnb": random.randint(0, 5),      # Number of downlink datagrams received
                "txnb": random.randint(0, 5),      # Number of packets emitted
                "temp": random.uniform(20.0, 35.0), # Gateway temperature (°C)
                "boot": "2024-08-27 10:00:00 GMT",  # Gateway boot time
                "hal": "5.0.1",   # Hardware abstraction layer version
                "fpga": 49,       # FPGA version
                "dsp": 37         # DSP version
            }
        }
        
        await self.websocket.send(json.dumps(stats_msg))
        logger.info("Sent gateway statistics")
    
    async def uplink_sender(self):
        """Periodically send uplink messages"""
        while self.running:
            try:
                await self.send_uplink()
                await asyncio.sleep(60)  # Send every 60 seconds
            except Exception as e:
                logger.error(f"Uplink sender error: {e}")
                break
    
    async def stats_sender(self):
        """Periodically send gateway statistics"""
        while self.running:
            try:
                await self.send_stats()
                await asyncio.sleep(30)  # Send stats every 30 seconds
            except Exception as e:
                logger.error(f"Stats sender error: {e}")
                break
    
    async def run(self):
        """Main simulation loop"""
        while True:
            try:
                # Connect to ChirpStack
                if not await self.connect():
                    logger.error("Failed to connect, retrying in 10 seconds...")
                    await asyncio.sleep(10)
                    continue
                
                # Send initial handshake
                await self.send_version()
                await asyncio.sleep(1)
                await self.send_router_info()
                await asyncio.sleep(1)
                
                self.running = True
                logger.info("Gateway simulator started - should appear online in ChirpStack")
                
                # Start concurrent tasks
                tasks = [
                    asyncio.create_task(self.message_handler()),
                    asyncio.create_task(self.uplink_sender()),
                    asyncio.create_task(self.stats_sender())
                ]
                
                # Wait for any task to complete (usually due to error)
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                
                # Cancel remaining tasks
                for task in pending:
                    task.cancel()
                
                self.running = False
                
                # Close connection
                if self.websocket:
                    await self.websocket.close()
                
                logger.warning("Connection lost, reconnecting in 10 seconds...")
                await asyncio.sleep(10)
                
            except KeyboardInterrupt:
                logger.info("Simulator stopped by user")
                self.running = False
                if self.websocket:
                    await self.websocket.close()
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                await asyncio.sleep(10)

async def main():
    """Main entry point"""
    simulator = ChirpStackGatewaySimulator()
    
    print("🚀 ChirpStack Gateway Simulator")
    print(f"   Gateway EUI: {GATEWAY_EUI}")
    print(f"   ChirpStack Server: {CHIRPSTACK_SERVER}")
    print("   Starting simulation...")
    print("\n⚠️  Make sure:")
    print("   1. ChirpStack is running with Basic Station enabled")
    print("   2. Gateway is registered in ChirpStack with matching EUI")
    print("   3. Install websockets: pip install websockets")
    print("\n🔄 Connecting...")
    
    await simulator.run()

if __name__ == "__main__":
    asyncio.run(main())
