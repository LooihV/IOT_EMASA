import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ocpp.routing import on
from ocpp.v16 import ChargePoint
from ocpp.v16 import call_result

logging.basicConfig(level=logging.INFO)

class ChargePointHandler(ChargePoint):
    """ Implementa los métodos OCPP """
    
    @on("BootNotification")  
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        """ Responde a un BootNotification correctamente """
        logging.info("📩 BootNotification recibido y procesado.")
        try:
            response = call_result.BootNotification(
                current_time="2025-02-25T12:34:56Z",
                interval=10,
                status="Accepted",
            )
            logging.info(f"✅ Respuesta enviada: {response}")  # ✅ Agrega logs para verificar el resultado
            return response
        except Exception as e:
            logging.error(f"⚠️ Error en BootNotification: {e}")
            return call_result.BootNotification(
                current_time="2025-02-25T12:34:56Z",
                interval=10,
                status="Rejected",
            )

class OCPPConsumer(AsyncWebsocketConsumer):
    """ Maneja conexiones WebSocket con el protocolo OCPP """

    async def connect(self):
        """ Se ejecuta cuando un sensor intenta conectarse """
        self.id = self.scope["path"]  
        self.cp = ChargePointHandler(self.id, self)  # ✅ Usa ChargePointHandler en lugar de ChargePoint
        await self.accept()
        logging.info(f"✅ Sensor conectado: {self.id}")

    async def disconnect(self, close_code):
        """ Se ejecuta cuando el sensor se desconecta """
        logging.info(f"❌ Sensor desconectado: {self.id}")

    async def receive(self, text_data=None, bytes_data=None):
        """ Maneja mensajes entrantes """
        try:
            message = json.loads(text_data)
            logging.info(f"📩 Mensaje recibido: {message}")
            await self.cp.route_message(json.dumps(message))  # ✅ Convierte el mensaje a JSON antes de enviarlo
        except Exception as e:
            logging.error(f"⚠️ Error al procesar mensaje: {e}")
            await self.send(json.dumps({"error": str(e)}))  # ✅ Enviar error al cliente