import asyncio
import json
import os
import sys

import django
import serial_asyncio
import websockets
from asgiref.sync import sync_to_async
from serial.tools import list_ports

# set current dir to same as django so imports are possible
current_dir = os.path.dirname(os.path.abspath(__file__))
server_comm_dir = os.path.join(current_dir, "server_comm")
os.chdir(server_comm_dir)
sys.path.append(server_comm_dir)

# set up django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server_comm.settings')
django.setup()

# import view from django
from device_connection.views import FlowDeviceConnectionView  # type: ignore


async def adb_log_stream(adb_device_id):
    process = await asyncio.create_subprocess_exec(
        "adb",
        "-s",
        adb_device_id,
        "logcat",
        stdout=asyncio.subprocess.PIPE,
    )

    try:
        while True:
            log_line = await process.stdout.readline()
            if not log_line:
                await asyncio.sleep(0.1)
                continue
            yield log_line.decode('utf-8').strip()

    except asyncio.CancelledError:
        print(f"ADB log stream for {adb_device_id} was closed")

    except Exception as e:
        print(
            f"Error occurred while logging adb device {adb_device_id}: {str(e)}"
        )

    finally:
        process.terminate()
        await process.wait()


async def uart_log_stream(serial_number):
    def get_device_port(serial_number: str):
        ports = list_ports.comports()
        for port in ports:
            if port.serial_number == serial_number:
                return port.device
        return None

    device_port = get_device_port(serial_number)
    if not device_port:
        print(f"No port detected for serial number {serial_number}")
        return

    reader, _ = await serial_asyncio.open_serial_connection(url=device_port)

    try:
        while True:
            line = await reader.readline()
            yield line

    except asyncio.CancelledError:
        print(f"UART log stream for {serial_number} was closed")

    except Exception as e:
        print(
            f"Error occurred while logging UART device {serial_number}: {str(e)}"
        )

    finally:
        reader.close()


async def stream_device_log(
    websocket, device_id, device_name, conn_type, conn_id, log_id
):
    match conn_type:
        case "adb":
            log_stream = adb_log_stream
        case "uart":
            log_stream = uart_log_stream
        case _:
            print(f"Unsupported connection type: {conn_type}")
            return

    try:
        async for line in log_stream(conn_id):
            log_entry = {
                "id": log_id,
                "name": f"{device_name} - {conn_type}",
                "log": (
                    line.decode("utf-8").strip()
                    if isinstance(line, bytes)
                    else line
                ),
            }
            log_message = json.dumps(log_entry)
            await websocket.send(log_message)

    except websockets.ConnectionClosed:
        print(f"Connection closed for {device_name} (ID: {device_id})")


async def log_all(websocket, path):
    # parse flow_id from path
    flow_id = path.split("/")[-1]
    print(f"Server connected, logging for flow {flow_id}")

    flow_view = FlowDeviceConnectionView()
    devices_conn, _, devices_name = await sync_to_async(
        flow_view.parse_devices
    )(flow_id)

    # log counter to give ids to each log
    log_ids = {}
    current_log_id = 1
    for device_id in devices_name:
        log_ids.setdefault(device_id, {})
        for conn_type in devices_conn[device_id].keys():
            log_ids[device_id].setdefault(conn_type, current_log_id)
            current_log_id += 1

    # one task per device per connection type
    tasks = []
    for device_id in devices_name:
        device_name: str = devices_name[device_id]
        device_conn: list = devices_conn[device_id]

        for conn_type, conn_id in device_conn.items():
            log_id = log_ids[device_id][conn_type]
            tasks.append(
                stream_device_log(
                    websocket,
                    device_id,
                    device_name,
                    conn_type,
                    conn_id,
                    log_id,
                )
            )

    await asyncio.gather(*tasks)


async def main():
    async with websockets.serve(log_all, "localhost", 8765):
        print("Websocket startet running on port 8765")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
