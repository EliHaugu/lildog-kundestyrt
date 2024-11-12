import json

import pytest
import websockets
from conftest import WEBSOCKET_URL


@pytest.mark.asyncio
async def test_load_logs(start_server):
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        log_msg = await websocket.recv()
        log_data = json.loads(log_msg)['message']
        assert (
            log_data == "Connected to websocket!"
        ), "Could not connect to server"


@pytest.mark.asyncio
async def test_invalid_flow_id(start_server):
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        _ = await websocket.recv()
        flow_error_msg = await websocket.recv()
        flow_error_data = json.loads(flow_error_msg)['error']
        assert flow_error_data == "Missing or invalid flow ID"
