import json

from channels.generic.websocket import WebsocketConsumer # type: ignore


class LogConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        device_id = text_data_json['deviceId']

        # Simulate fetching logs for the device
        logs = [
            {'id': device_id, 'name': 'Device A', 'log': ['Log 1', 'Log 2']}
        ]

        # Send logs back to WebSocket client
        self.send(text_data=json.dumps(logs))
