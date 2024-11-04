import os
import subprocess


def run_check_connection(
    android_device_id,
    mac_address,
):
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)

    command = [
        "./test.sh",
        "-d",
        android_device_id,
        "-e",
        "MAC_ADDRESS",
        mac_address,
        "connection.xml",
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)


def run_check_service(
    android_device_id,
    mac_address,
    service_uuid,
):
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)

    command = [
        "./test.sh",
        "-d",
        android_device_id,
        "-e",
        "MAC_ADDRESS",
        mac_address,
        "-e",
        "SERVICE_UUID",
        service_uuid,
        "check_service.xml",
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)


def run_check_characteristic(
    android_device_id,
    mac_address,
    service_uuid,
    characteristic_uuid,
):
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)

    command = [
        "./test.sh",
        "-d",
        android_device_id,
        "-e",
        "MAC_ADDRESS",
        mac_address,
        "-e",
        "SERVICE_UUID",
        service_uuid,
        "-e",
        "CHARACTERISTIC_UUID",
        characteristic_uuid,
        "check_characteristic.xml",
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)


def run_custom_script(android_device_id, mac_address, extras):
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)

    extra_cmd = []
    for var, value in extras.items():
        extra_cmd.append("-e")
        extra_cmd.append(var)
        extra_cmd.append(value)

    command = [
        "./test.sh",
        "-d",
        android_device_id,
        "-e",
        "MAC_ADDRESS",
        mac_address,
    ]
    command.extend(extra_cmd)
    command.append("custom_script.xml")

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)
