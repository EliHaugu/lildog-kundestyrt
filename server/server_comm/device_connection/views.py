from django.http import JsonResponse
from django.views import View
import serial
import time

class SerialDeviceConnectionView(View):
    def check_connection(self, request, device_port: str):
        try:
            serial_device = serial.Serial(device_port)
            serial_device.write(b'ping\n')
            time.sleep(1)
            res = serial_device.readline().strip()
            
            if res == b'pong':
                return JsonResponse({'status': 'connected', 'message': 'UART device connected!'})
            else:
                return JsonResponse({'status': 'unexpected_response', 'message': res})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
