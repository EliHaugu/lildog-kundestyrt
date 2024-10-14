import serial
import time

def check_connection(device_port: str):
    serial_device = serial.Serial(device_port)

    while True:
        try:
            serial_device.write(b'ping\n')
            time.sleep(1)
            res = serial_device.readline().strip()
            
            if res == b'pong':
                print(f"Device {device_port} connected!")
            else:
                print(f"Unexpected response from device {device_port}: {res}")
        except Exception as e:
            print(f"Error: Could not establish connection to UART device on port: {device_port}\nError: {e}")
    
    print("Connected!")

