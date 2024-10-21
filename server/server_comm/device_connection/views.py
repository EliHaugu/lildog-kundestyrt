import subprocess
import time

from consts import conn_type_id_mapping
from data_manager.models import Flow
from django.http import JsonResponse
from django.views import View
from serial import Serial
from serial.tools import list_ports


class SerialDeviceConnectionView(View):
    def get_device_port(self, conn_id: str):
        ports = list_ports.comports()
        for port in ports:
            if port.serial_number == conn_id:
                return port.device
        return None

    def check_connection(self, conn_id: str):
        try:
            device_port = self.get_device_port(conn_id)
            serial_device = Serial(device_port)

            serial_device.write(b'ping\n')
            time.sleep(1)
            res = serial_device.readline().strip()

            if res:
                return JsonResponse(
                    {
                        'status': 'connected',
                        'message': 'serial device connected',
                        'response': res,
                    }
                )
            else:
                return JsonResponse(
                    {
                        'status': 'no_response',
                        'message': 'serial device did not respond',
                        'response': None,
                    }
                )
        except Exception as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'an error occurred',
                    'response': str(e),
                }
            )


class AndroidDeviceConnectionView(View):
    def get_adb_devices(self):
        try:
            adb_devices = subprocess.run(
                ['adb', 'devices'], capture_output=True, text=True, check=True
            ).stdout.splitlines()[1:-1]
            adb_devices = [line.split("\t")[0] for line in adb_devices]
            return adb_devices

        except subprocess.CalledProcessError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'adb command failed',
                    'response': str(e),
                }
            )

        except FileNotFoundError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'adb not found',
                    'response': str(e),
                }
            )

        except Exception as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'an error occurred',
                    'response': str(e),
                }
            )

    def check_connection(self, conn_id: str):
        adb_devices = self.get_adb_devices()

        if conn_id in adb_devices:
            return JsonResponse(
                {
                    'status': 'connected',
                    'message': 'android device connected',
                    'response': None,
                }
            )
        else:
            return JsonResponse(
                {
                    'status': 'not_connected',
                    'message': 'android device not connected',
                    'response': None,
                }
            )


class FlowDeviceConnectionView(View):
    def parse_devices(self, request):
        flow_id = request.GET.get('flow_id')
        flow = Flow.objects.get(id=flow_id)
        devices = {}

        for node in flow.nodes.all():
            device = node.device
            device_id = device.device_id
            category = device.category
            devices.setdefault(device_id, [])

            connection_types = category.connection_types
            for conn_type in connection_types:
                conn_id_field = conn_type_id_mapping[conn_type]
                conn_id = device.connection_ids.get(conn_id_field)
                devices[device_id].append((conn_type, conn_id))

        return devices

    def connect_devices(self, flow_id: str):
        devices = self.parse_devices(flow_id)

        for connection_info in devices.values():
            for conn in connection_info:
                conn_type = conn[0]
                conn_id = conn[1]

                match conn_type:
                    case "uart":
                        serial_view = SerialDeviceConnectionView()
                        serial_view.check_connection(conn_id)