import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TemperatureConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("temperature_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("temperature_updates", self.channel_name)

    async def receive(self, text_data):
        pass

    async def temperature_update(self, event):
        await self.send(text_data=json.dumps({
            "temperature": event.get("temperature"),
            "humidity": event.get("humidity"),
            "heat_index": event.get("heat_index"),
        }))
