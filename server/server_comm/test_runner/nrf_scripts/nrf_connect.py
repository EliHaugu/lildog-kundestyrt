import os
import subprocess


def run_command(name, command, filename):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        stdout, stderr = result.stdout, result.stderr
    except Exception as e:
        return {
            "status": "error",
            "message": f"Exception occurred while executing command: {name}",
            "response": str(e),
        }

    if stderr:
        return {
            "status": "error",
            "message": f"Error occurred while running command: {name}",
            "response": stderr,
        }

    if "Error" in stdout:
        return {
            "status": "error",
            "message": f"Error occurred while running command: {name}",
            "response": stdout,
        }

    with open(filename, "r") as file:
        lines = file.readlines()

    if "completed" in lines[-1]:
        return {
            "status": "success",
            "message": f"Command: {name}, ran successfully",
            "response": "",
        }

    for i in range(len(lines)):
        if name in lines[i]:
            start_idx = i
            break

    error_lines = []
    for line in lines[start_idx:]:
        line = line.split("\t")
        if line[0] == "E" or line[0] == "W":
            error_lines.append(line)

    return {
        "status": "error",
        "message": f"nRF script: {name}, failed",
        "response": error_lines,
    }


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

    return run_command("Connect", command, "connection_result.txt")


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

    return run_command(
        "Check Service UUID", command, "check_service_result.txt"
    )


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

    return run_command(
        "Check Characteristic UUID", command, "check_characteristic_result.txt"
    )


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

    return run_command("Custom script", command, "custom_script_result.txt")
