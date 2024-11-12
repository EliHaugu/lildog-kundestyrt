import socket
import subprocess
import time

import pytest

HOST = "localhost"
PORT = 8765
SERVER_TIMEOUT = 5
WEBSOCKET_URL = f"ws://{HOST}:{PORT}"


def poll_server(host=HOST, port=PORT, timeout=SERVER_TIMEOUT):
    """Poll server until connection is established"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(0.1)
    raise TimeoutError("Server did not start within the expected timeout")


@pytest.fixture()
def start_server():
    process = subprocess.Popen(["python", "server.py"])
    poll_server()
    yield
    process.terminate()
    process.wait()
