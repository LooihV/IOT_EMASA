import logging
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result

logging.basicConfig(level=logging.INFO)


class OCPPConsumer(cp, AsyncWebsocketConsumer):
    """ Maneja conexiones WebSocket OCPP """

    async def connect(self):
        """ Se ejecuta cuando un sensor intenta conectarse """
        self.id = self.scope["path"]  # Usamos la URL como identificador
        await self.accept()  # Aceptamos la conexión
        logging.info(f"✅ Sensor conectado: {self.id}")

    async def disconnect(self, close_code):
        """ Se ejecuta cuando el sensor se desconecta """
        logging.info(f"❌ Sensor desconectado: {self.id}")

    async def receive(self, text_data=None, bytes_data=None):
        """ Maneja mensajes entrantes """
        try:
            message = json.loads(text_data)
            logging.info(f"📩 Mensaje recibido: {message}")
            await self.route_message(message)
        except Exception as e:
            logging.error(f"⚠️ Error al procesar mensaje: {e}")

    @on("BootNotification")
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        """ Responde a un BootNotification """
        return call_result.BootNotificationPayload(
            current_time="2025-02-25T12:34:56Z",
            interval=10,
            status="Accepted",
        )