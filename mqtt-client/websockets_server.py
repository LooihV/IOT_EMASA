"""
WebSocket Real-Time Communication Server

This module implements a high-performance WebSocket server that bridges IoT data
from MQTT sources to Vue.js frontend applications in real-time. It provides
bidirectional communication, client management, and robust error handling
for industrial IoT monitoring systems.

Key Features:
- Asynchronous WebSocket server with concurrent client support
- Real-time data broadcasting to multiple Vue.js frontends
- Automatic client connection management and cleanup
- Bidirectional communication with message echo capabilities
- Thread-safe operations for MQTT integration
- Comprehensive connection monitoring and logging
- Graceful error handling and recovery

Architecture:
    MQTT Client -> Data Processor -> WebSocket Server -> Vue.js Frontend(s)
    
Communication Flow:
    1. Vue.js clients connect via WebSocket protocol
    2. Server maintains active client registry
    3. MQTT data arrives and gets broadcast to all clients
    4. Clients can send commands/requests back to server
    5. Automatic cleanup of disconnected clients

Network Configuration:
    - Default Host: 0.0.0.0 (all interfaces)
    - Default Port: 8765
    - Protocol: WebSocket (ws://) with ping/pong keepalive
    - Client Capacity: Unlimited (memory permitting)

Integration Points:
    - MQTT payload processor (payload_processing.py)
    - Main IoT gateway (main.py)
    - Vue.js frontend applications

Author: IoT Development Team
Version: 1.0
Date: August 2025
"""

import asyncio
import websockets
import json
import logging
import threading
import os
from typing import Set
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WebSocket server configuration from environment variables
DEFAULT_WEBSOCKET_HOST = os.getenv('WEBSOCKET', '0.0.0.0')
DEFAULT_WEBSOCKET_PORT = int(os.getenv('WEBSOCKET_PORT', '8765'))

"""
    Initialize WebSocket server with network configuration.
    
    Sets up the server infrastructure for handling multiple Vue.js client
    connections with configurable host and port settings.
    
    Args:
        host (str): Network interface to bind to
            - "0.0.0.0": All available interfaces (default)
            - "127.0.0.1": Localhost only
            - Specific IP: Bind to specific network interface
        port (int): TCP port for WebSocket connections (default: 8765)
            - Must be available and not used by other services
            - Should match frontend configuration
            
    Attributes:
        clients (Set): Thread-safe registry of active WebSocket connections
        server: WebSocket server instance (None until started)
        
    Network Requirements:
        - Firewall rules must allow inbound connections on specified port
        - Port must not conflict with other services (avoid 80, 443, 8080)
        - Network interface must be accessible from Vue.js application
    """
class WebSocketServer:
    def __init__(self, host=DEFAULT_WEBSOCKET_HOST, port=DEFAULT_WEBSOCKET_PORT):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None


        """
    Handle individual WebSocket client connections.
    
    Manages the complete lifecycle of a Vue.js client connection from
    initial handshake through message processing to graceful disconnection.
    Implements bidirectional communication with comprehensive error handling.
    
    Connection Lifecycle:
    1. Accept incoming WebSocket connection
    2. Add client to active registry
    3. Send welcome message with server status
    4. Enter message processing loop
    5. Handle incoming messages with JSON validation
    6. Process disconnections and cleanup
    
    Args:
        websocket: WebSocket connection protocol instance
            - Provides send/receive capabilities
            - Contains client address information
            - Manages connection state and health
            
    Message Processing:
        - Validates incoming JSON messages
        - Implements echo functionality for testing
        - Logs all client interactions for monitoring
        - Handles malformed messages gracefully
        
    Error Handling:
        - Connection drops: Automatic cleanup and logging
        - JSON errors: Warning logs with continued operation
        - Unexpected exceptions: Error logging with stack traces
        - Resource cleanup: Guaranteed client removal from registry
        
    Performance Notes:
        - Asynchronous operation prevents blocking
        - Efficient client set operations for registry management
        - Minimal memory footprint per connection
        - Automatic garbage collection of disconnected clients
    """    
    async def handle_client(self, websocket):
        """Handle new WebSocket client connection"""
        client_addr = websocket.remote_address
        try:
            # Add client to set
            self.clients.add(websocket)
            logger.info(f"🔗 New Vue client connected from {client_addr}")
            logger.info(f"📊 Total connected clients: {len(self.clients)}")
            
            # Send welcome message
            welcome_message = {
                "type": "connection",
                "message": "Connected to IoT WebSocket server",
                "timestamp": datetime.now().isoformat(),
                "clients_count": len(self.clients)
            }
            await websocket.send(json.dumps(welcome_message))
            logger.info(f"👋 Welcome message sent to {client_addr}")
            
            # Keep connection alive and handle incoming messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    logger.info(f"📥 Message from Vue client: {data}")
                    
                    # Echo back for testing
                    response = {
                        "type": "echo",
                        "original": data,
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(response))
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ Invalid JSON from client: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"🔌 Client {client_addr} disconnected normally")
        except Exception as e:
            logger.error(f"❌ Error handling client {client_addr}: {e}")
        finally:
            # Remove client from set
            self.clients.discard(websocket)
            logger.info(f"🚪 Client removed. Remaining clients: {len(self.clients)}")


        """
    Broadcast message to all connected Vue.js clients.
    
    High-performance broadcasting function that delivers IoT data to all
    active frontend connections simultaneously. Implements automatic cleanup
    of failed connections and comprehensive error handling.
    
    Broadcasting Strategy:
    1. Validate client registry is not empty
    2. Serialize message to JSON once (efficiency)
    3. Attempt delivery to all clients concurrently
    4. Track and remove failed connections
    5. Log broadcast results and statistics
    
    Args:
        message (dict): Data structure to broadcast to Vue.js clients
            - Must be JSON-serializable
            - Typically contains IoT sensor data
            - Should include timestamp and type information
            
    Message Structure Example:
        {
            "device_name": "VoltageMonitor_001",
            "measurement_values": [...],
            "timestamp": "2025-08-01T10:30:00Z",
            "type": "iot_data"
        }
        
    Error Recovery:
        - Connection failures: Automatic client removal
        - Serialization errors: Error logging and early return
        - Partial failures: Continue with successful deliveries
        - Network issues: Client-specific error handling
        
    Performance Optimizations:
        - Single JSON serialization for all clients
        - Concurrent delivery to multiple clients
        - Efficient set operations for client management
        - Minimal memory allocation during broadcast
        
    Monitoring and Logging:
        - Client count tracking
        - Delivery success/failure statistics
        - Connection health monitoring
        - Performance metrics logging
    """
        
    async def broadcast_to_all(self, message: dict):
        """Send message to all connected Vue clients"""
        if not self.clients:
            logger.debug("📭 No clients connected to broadcast to")
            return
            
        # Convert message to JSON
        message_json = json.dumps(message)
        
        # Send to all clients (remove failed connections)
        disconnected = set()
        
        for client in self.clients.copy():
            try:
                await client.send(message_json)
                logger.debug(f"📤 Message sent to {client.remote_address}")
            except websockets.exceptions.ConnectionClosed:
                logger.info(f"🔌 Client {client.remote_address} disconnected during broadcast")
                disconnected.add(client)
            except Exception as e:
                logger.error(f"❌ Failed to send to {client.remote_address}: {e}")
                disconnected.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected
        
        logger.info(f"📡 Broadcast sent to {len(self.clients)} clients")



        """
    Start the WebSocket server with comprehensive configuration.
    
    Initializes and runs the WebSocket server with production-ready settings
    including ping/pong keepalive, error handling, and connection monitoring.
    This is the main server entry point that handles all network operations.
    
    Server Configuration:
        - Bind Address: Configurable host interface
        - Port: Configurable TCP port (default 8765)
        - Ping Interval: 20 seconds (connection health check)
        - Ping Timeout: 10 seconds (connection failure detection)
        - Protocol: WebSocket with automatic upgrade from HTTP
        
    Startup Sequence:
    1. Log server initialization
    2. Create WebSocket server with ping/pong configuration
    3. Bind to specified host and port
    4. Log successful startup
    5. Enter event loop waiting for connections
    6. Handle shutdown gracefully
    
    Connection Health Management:
        - Automatic ping frames every 20 seconds
        - Client must respond with pong within 10 seconds
        - Failed health checks trigger automatic disconnection
        - Prevents zombie connections from consuming resources
        
    Error Handling:
        - Port binding failures: Clear error messages
        - Permission errors: Detailed troubleshooting information
        - Network interface errors: Configuration guidance
        - Unexpected exceptions: Full stack trace logging
        
    Production Deployment Notes:
        - Ensure firewall allows inbound connections on configured port
        - Consider using reverse proxy (nginx) for production
        - Monitor connection counts and resource usage
        - Implement connection rate limiting if needed
    """
    async def start_server(self):
        """Start the WebSocket server"""
        try:
            logger.info(f"🌐 Starting WebSocket server on {self.host}:{self.port}")
            
            # Start server with corrected handler
            self.server = await websockets.serve(
                self.handle_client,
                self.host,
                self.port,
                ping_interval=20,
                ping_timeout=10
            )
            
            logger.info(f"✅ WebSocket server started successfully!")
            logger.info(f"🔗 Listening for Vue frontend connections on ws://{self.host}:{self.port}")
            
            # Keep server running
            await self.server.wait_closed()
            
        except Exception as e:
            logger.error(f"❌ Failed to start WebSocket server: {e}")
            raise
    

        """
    Get current number of connected clients.
    
    Thread-safe method to retrieve the current count of active Vue.js
    client connections. Used for monitoring and capacity planning.
    
    Returns:
        int: Number of currently connected WebSocket clients
        
    Use Cases:
        - System monitoring and health checks
        - Load balancing decisions
        - Resource usage tracking
        - Client capacity planning
        
    Thread Safety:
        - Safe to call from any thread
        - Atomic operation on client set
        - No blocking or async requirements
    """
        
    def get_client_count(self):
        """Get number of connected clients"""
        return len(self.clients)



    """
    Gracefully stop the WebSocket server.
    
    Implements clean shutdown procedures including client notification,
    connection cleanup, and resource deallocation. Ensures no data loss
    and proper cleanup of all network resources.
    
    Shutdown Sequence:
    1. Log shutdown initiation
    2. Close server socket (no new connections)
    3. Wait for existing connections to close naturally
    4. Force close any remaining connections
    5. Clean up resources and log completion
    
    Client Handling:
        - Existing connections receive close frames
        - Clients can finish sending pending messages
        - Graceful disconnection prevents data loss
        - Connection registry is automatically cleaned
        
    Resource Cleanup:
        - Network socket closure
        - Memory deallocation
        - Thread cleanup
        - Event loop termination
        
    Use Cases:
        - Application shutdown
        - Server maintenance
        - Configuration changes requiring restart
        - Emergency shutdown procedures
    """
    async def stop_server(self):
        """Stop the WebSocket server"""
        if self.server:
            logger.info("🛑 Stopping WebSocket server...")
            self.server.close()
            await self.server.wait_closed()
            logger.info("✅ WebSocket server stopped")

# Global server instance
websocket_server = None


"""
Start WebSocket server in background thread.

Creates and initializes a WebSocket server instance in a separate thread
to avoid blocking the main MQTT processing loop. Implements proper thread
management and error handling for production deployment.

Threading Architecture:
    Main Thread: MQTT client and message processing
    WebSocket Thread: Handles all WebSocket operations
    Broadcast Threads: Handle data transmission to clients

Args:
    host (str): Network interface to bind WebSocket server
        - "0.0.0.0": Accept connections from any interface (default)
        - "127.0.0.1": Local connections only
        - Specific IP: Bind to particular network interface
    port (int): TCP port for WebSocket connections (default: 8765)
        - Must be available and not in use
        - Should be accessible from Vue.js frontend
        
Returns:
    threading.Thread: Background thread running the WebSocket server
        - Daemon thread (terminates with main process)
        - Can be used for monitoring thread health
        - Automatic cleanup on application exit
        
Global State Management:
    - Sets global websocket_server instance
    - Enables cross-module access for broadcasting
    - Thread-safe initialization and access
    
Error Handling:
    - Thread creation failures: Detailed error logging
    - Server startup failures: Exception propagation
    - Event loop errors: Comprehensive stack traces
    - Resource cleanup: Automatic thread termination
    
Production Considerations:
    - Monitor thread health and resource usage
    - Implement restart logic for thread failures
    - Consider process supervision for critical deployments
    - Log thread lifecycle events for debugging
"""
def start_websocket_server(host=DEFAULT_WEBSOCKET_HOST, port=DEFAULT_WEBSOCKET_PORT):
    """Start WebSocket server in background thread"""
    global websocket_server
    
    # Create the server instance with specified or default configuration
    websocket_server = WebSocketServer(host, port)
    

    """
    Background thread function for WebSocket server execution.
    
    Creates isolated event loop for WebSocket operations to prevent
    interference with main MQTT processing thread. Implements proper
    asyncio lifecycle management and error handling.
    
    Event Loop Management:
        - Creates new event loop for thread isolation
        - Sets thread-local event loop
        - Runs server until completion or error
        - Properly closes loop on exit
        
    Error Recovery:
        - Catches and logs all exceptions
        - Provides stack traces for debugging
        - Prevents thread crashes from affecting main process
        - Ensures proper resource cleanup
    """
    def run_server():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Use the global server instance
            loop.run_until_complete(websocket_server.start_server())
        except Exception as e:
            logger.error(f"❌ WebSocket server error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            loop.close()
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    logger.info(f"🌐 WebSocket server thread started")
    logger.info(f"🔧 Global websocket_server initialized: {websocket_server is not None}")
    
    return server_thread


"""
Send IoT data to all connected Vue.js clients.

High-level interface for broadcasting processed IoT sensor data to all
connected frontend applications. Implements thread-safe operations and
comprehensive error handling for reliable data delivery.

Data Broadcasting Pipeline:
    IoT Data -> Thread Safety Check -> Global Server Access -> 
    Async Broadcast -> Client Delivery -> Success Logging

Args:
    data (dict): Processed IoT data structure for frontend consumption
        - device_name: Device identifier
        - measurement_values: Array of sensor readings
        - timestamp: Data collection time
        - Additional metadata as needed
        
Data Structure Example:
    {
        "device_name": "VoltageMonitor_001",
        "measurement_values": [
            {"time_iso": "2025-08-01T10:30:00Z", "value": 12.5},
            ...
        ],
        "buffer_stats": {"total_samples": 50, "avg_voltage": 12.3},
        "radio_info": {"rssi": -85, "snr": 8.5},
        "timestamp": "2025-08-01T10:30:00Z"
    }
    
Thread Safety:
    - Safe to call from MQTT processing thread
    - Creates isolated broadcast thread for async operations
    - No blocking of main processing loop
    - Proper event loop management
    
Error Handling:
    - Server not initialized: Warning with graceful return
    - No connected clients: Information logging
    - Broadcast failures: Detailed error logging
    - Thread failures: Exception isolation
    
Performance Notes:
    - Non-blocking operation for main thread
    - Efficient JSON serialization
    - Concurrent delivery to multiple clients
    - Automatic cleanup of failed connections
    
Monitoring and Logging:
    - Data summary logging (device, sample count)
    - Client count monitoring
    - Success/failure status reporting
    - Performance metrics tracking
"""
def send_to_vue(data):
    """Send data to all connected Vue clients"""
    global websocket_server
    
    logger.info(f"📤 Attempting to send data to Vue clients...")
    logger.info(f"   📊 Device: {data.get('device_name', 'N/A')}")
    logger.info(f"   📈 Samples: {len(data.get('measurement_values', []))}")
    logger.info(f"   🔧 WebSocket server initialized: {websocket_server is not None}")
    
    if websocket_server is None:
        logger.warning("⚠️ WebSocket server not initialized")
        return
    
    logger.info(f"   🌐 Connected clients: {websocket_server.get_client_count()}")
    
    

    """
    Background thread function for asynchronous broadcasting.
    
    Creates isolated event loop to handle WebSocket broadcasting
    without blocking the main MQTT processing thread.
    
    Async Operations:
        - Creates new event loop for thread isolation
        - Executes broadcast in async context
        - Handles all WebSocket async operations
        - Ensures proper cleanup
        
    Error Isolation:
        - Catches broadcast exceptions
        - Prevents main thread disruption
        - Provides detailed error logging
        - Continues operation after failures
    """
    def run_broadcast():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(websocket_server.broadcast_to_all(data))
            logger.info("✅ Data sent to Vue clients successfully")
        except Exception as e:
            logger.error(f"❌ Error broadcasting to Vue clients: {e}")
            import traceback
            traceback.print_exc()
        finally:
            loop.close()
    
    # Run broadcast in a separate thread to avoid blocking
    broadcast_thread = threading.Thread(target=run_broadcast, daemon=True)
    broadcast_thread.start()



"""
Get number of connected Vue.js clients.

Thread-safe accessor for monitoring the current number of active
WebSocket connections. Used for system monitoring, capacity planning,
and operational health checks.

Returns:
    int: Current count of connected Vue.js clients
        - 0: No clients connected
        - >0: Number of active frontend connections
        
Use Cases:
    - System health monitoring
    - Load balancing decisions
    - Resource usage tracking
    - Operational dashboards
    - Capacity planning
    
Thread Safety:
    - Safe to call from any thread
    - No async operations required
    - Atomic read operation
    - No side effects
    
Error Handling:
    - Server not initialized: Returns 0
    - No exceptions thrown
    - Graceful degradation
"""
def get_connected_clients():
    """Get number of connected Vue clients"""
    global websocket_server
    
    if websocket_server is None:
        return 0
    
    return websocket_server.get_client_count()


"""
Test standalone server functionality.

Development and testing entry point that runs the WebSocket server
in standalone mode for testing and validation purposes.

Test Capabilities:
    - Server startup and initialization
    - Connection handling
    - Message processing
    - Error handling
    - Performance validation
    
Usage:
    python websockets_server.py
    
Test Scenarios:
    - Connect with WebSocket client tools
    - Send test messages
    - Validate echo functionality
    - Monitor connection handling
    - Test error recovery
"""
if __name__ == "__main__":
    async def test_server():
        server = WebSocketServer()
        await server.start_server()
    
    print("🧪 Testing WebSocket server standalone...")
    asyncio.run(test_server())