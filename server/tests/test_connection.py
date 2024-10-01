import json

import pytest
import websockets
from conftest import WEBSOCKET_URL


@pytest.mark.asyncio
async def test_load_logs(start_server):
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        log_message = await websocket.recv()
        log_data = json.loads(log_message)

        assert "id" in log_data, "Log entry should contain an 'id'"
        print(f"Received log with id: {log_data['id']}")
