import json
import subprocess
import time

import requests
from consts import comm_protocol_id_mapping, conn_type_id_mapping
from data_manager.models import Flow
from django.http import JsonResponse
from django.views import View
from serial import Serial, SerialTimeoutException
from serial.tools import list_ports
from test_runner.nrf_scripts.nrf_connect import run_check_connection


class SerialDeviceConnectionView(View):
    def get_device_port(self, conn_id: str):
        ports = list_ports.comports()
        for port in ports:
            if port.serial_number == conn_id:
                return port.device
        return None

    def ping_device(self, conn_id: str):
        try:
            device_port = self.get_device_port(conn_id)
            if not device_port:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "device port not found",
                        "response": None,
                    }
                )
            serial_device = Serial(device_port, timeout=10)

            serial_device.write(b"ping\n")
            time.sleep(1)
            line = serial_device.readline()
            res = (
                line.decode("utf-8").strip()
                if isinstance(line, bytes)
                else line
            )

            if res:
                return JsonResponse(
                    {
                        "status": "connected",
                        "message": "serial device connected",
                        "response": res,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "status": "no_response",
                        "message": "serial device did not respond",
                        "response": None,
                    }
                )
        except SerialTimeoutException as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "serial device timed out",
                    "response": str(e),
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "an error occurred",
                    "response": str(e),
                }
            )

    def check_connection(self, conn_id: str):
        ports = list_ports.comports()
        for port in ports:
            if port.serial_number == conn_id:
                return JsonResponse(
                    {
                        "status": "connected",
                        "message": "serial device connected",
                        "response": None,
                    }
                )
        return JsonResponse(
            {
                "status": "error",
                "message": "device port not found",
                "response": None,
            }
        )

    def get(self, request):
        conn_id = request.GET.get("conn_id")
        if conn_id:
            return self.check_connection(conn_id)
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "conn_id is required",
                    "response": None,
                }
            )


class AndroidDeviceConnectionView(View):
    def get_adb_devices(self):
        try:
            adb_devices = subprocess.run(
                ["adb", "devices"], capture_output=True, text=True, check=True
            ).stdout.splitlines()[1:-1]
            adb_devices = [line.split("\t")[0] for line in adb_devices]
            return adb_devices

        except subprocess.CalledProcessError as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "adb command failed",
                    "response": str(e),
                }
            )

        except FileNotFoundError as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "adb not found",
                    "response": str(e),
                }
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "an error occurred",
                    "response": str(e),
                }
            )

    def check_connection(self, conn_id: str):
        adb_devices = self.get_adb_devices()
        if not adb_devices:
            return JsonResponse(
                {
                    "status": "not_connected",
                    "message": "no android devices connected",
                    "response": None,
                }
            )

        if conn_id in adb_devices:
            return JsonResponse(
                {
                    "status": "connected",
                    "message": "android device connected",
                    "response": None,
                }
            )
        else:
            return JsonResponse(
                {
                    "status": "not_connected",
                    "message": "android device not connected",
                    "response": None,
                }
            )

    def get(self, request):
        conn_id = request.GET.get("conn_id")
        if conn_id:
            return self.check_connection(conn_id)
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "conn_id is required",
                    "response": None,
                }
            )


class APIConnectionView(View):
    def check_connection(self, api_url: str):
        try:
            res = requests.get(api_url, timeout=10)

            if res.status_code == 200:
                return JsonResponse(
                    {
                        "status": "connected",
                        "message": "connected to api",
                        "response": res.json(),
                    }
                )
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": (
                            f"unexpected api response {res.status_code}"
                        ),
                        "response": res.json(),
                    }
                )
        except requests.exceptions.Timeout as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "api request timed out",
                    "response": str(e),
                }
            )
        except requests.exceptions.ConnectionError as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "could not connect to api",
                    "response": str(e),
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "an error occurred",
                    "response": str(e),
                }
            )

    def get(self, request):
        api_url = request.GET.get("api_url")
        if api_url:
            return self.check_connection(api_url)
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "api_url is required",
                    "response": None,
                }
            )


class nRFConnectionView(View):
    def check_connection(self, adb_device_id: str, mac_address: str):
        res = run_check_connection(adb_device_id, mac_address)
        if res["status"] == "success":
            return JsonResponse(
                {
                    "status": "connected",
                    "message": f"adb device {adb_device_id} connected to nrf",
                    "response": res,
                }
            )
        else:
            return JsonResponse(res)

    def get(self, request):
        adb_device_id = request.GET.get("adb_device_id")
        mac_address = request.GET.get("mac_address")
        if adb_device_id and mac_address:
            return self.check_connection(adb_device_id, mac_address)
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "adb_device_id and mac_address is required",
                    "response": None,
                }
            )


class FlowDeviceConnectionView(View):
    def parse_devices(self, flow_id: int):
        flow = Flow.objects.get(id=flow_id)
        devices_conn: dict[str, dict] = {}
        devices_comm: dict[str, dict] = {}
        devices_name: dict[str, str] = {}

        for node in flow.nodes.all():
            if not node.device:
                continue
            device = node.device
            device_id = device.id
            device_name = device.device_id
            category = device.category
            devices_conn.setdefault(device_id, {})
            devices_comm.setdefault(device_id, {})

            connection_types = category.connection_types
            for conn_type in connection_types:
                conn_id_field = conn_type_id_mapping.get(conn_type)
                if (
                    conn_id_field
                    and conn_id_field in device.connection_ids.keys()
                ):
                    conn_id = device.connection_ids.get(conn_id_field)
                    devices_conn[device_id][conn_type] = conn_id

            communication_protocols = category.communication_protocols
            for comm_protocol in communication_protocols:
                comm_id_field = comm_protocol_id_mapping.get(comm_protocol)
                if (
                    comm_id_field
                    and comm_id_field in device.communication_ids.keys()
                ):
                    comm_id = device.communication_ids.get(comm_id_field)
                    devices_comm[device_id][comm_protocol] = comm_id

            devices_name[device_id] = device_name

        return devices_conn, devices_comm, devices_name

    def connect_devices(self, flow_id: int):
        devices_conn, devices_comm, _ = self.parse_devices(flow_id)
        responses = []

        for device in devices_conn:
            for conn_type in devices_conn[device]:
                conn_id = devices_conn[device][conn_type]

                match conn_type:
                    case "uart":
                        serial_view = SerialDeviceConnectionView()
                        res = serial_view.check_connection(conn_id)
                        responses.append(json.loads(res.content))
                    case "adb":
                        android_view = AndroidDeviceConnectionView()
                        res = android_view.check_connection(conn_id)
                        responses.append(json.loads(res.content))
                    case _:
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": "invalid connection type",
                                "response": None,
                            }
                        )

        return JsonResponse({"response": responses})

    def get(self, request):
        flow_id = request.GET.get("flow_id")
        if flow_id:
            return self.connect_devices(flow_id)
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "flow_id is required",
                    "response": None,
                }
            )
