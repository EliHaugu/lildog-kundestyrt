import json

from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        device_id = text_data_json['deviceId']

        # Simulate fetching logs for the device
        logs = [
            {'id': device_id, 'name': 'Device A', 'log': ['Log 1', 'Log 2']}
        ]

        # Send logs back to WebSocket client
        await self.send(text_data=json.dumps(logs))
