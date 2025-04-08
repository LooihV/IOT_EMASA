import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://localhost:8000/ws/ocpp/"  # Asegúrate de que la URL sea correcta
    async with websockets.connect(uri) as websocket:
        print("✅ Conectado al servidor WebSocket OCPP")

        # ✅ Formato correcto según OCPP 1.6 (debe ser una lista, no un dict)
        boot_notification = [
            2,  # messageTypeId (2 = CALL)
            "123456",  # uniqueId
            "BootNotification",  # action
            {  # payload
                "chargePointModel": "Sensor_XYZ",
                "chargePointVendor": "Emasa"
            }
        ]

        await websocket.send(json.dumps(boot_notification))  # ✅ Convertimos a JSON string
        response = await websocket.recv()
        print(f"📩 Respuesta del servidor: {response}")

# Ejecutar la función asincrónica
asyncio.run(test_connection())