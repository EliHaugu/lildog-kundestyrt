import asyncio
import websockets
import json

# Load mock logs
def load_logs():
    with open('./assets/mock_data.json', 'r') as file:
        logs = json.load(file)
    return logs["logItems"]

async def log(websocket):
    print("Server connected")

    logs = load_logs()

    for log_entry in logs:
        log_message = json.dumps(log_entry)
        await websocket.send(log_message)
        print(f"Server sent log {log_entry['id']}")

async def main():
    async with websockets.serve(log, "localhost", 8765):
        await asyncio.Future() # run forever

if __name__ == "__main__":
    asyncio.run(main())