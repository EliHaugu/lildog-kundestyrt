import os
import subprocess


def run_adb_test(
    android_device_id,
    target_uuid,
    extra_address,
    test_script,
    test_xml,
    result_file,
):
    if os.path.exists(result_file):
        os.remove(result_file)

    command = [
        test_script,
        "-d",
        android_device_id,
        "-E",
        "TARGET_UUID",
        target_uuid,
        "-E",
        "EXTRA_ADDRESS",
        extra_address,
        test_xml,
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)


def check_test_results(result_file):
    if not os.path.exists(result_file):
        return None, "Result file not found"

    try:
        with open(result_file, 'r') as file:
            content = file.read()

            if "FAIL" in content:
                return False, "Test failed"
            else:
                return True, "Test passed"
    except Exception as e:
        return None, str(e)


if __name__ == "__main__":
    test_bat = 'test.bat'  # For linux/Mac use '\.test.sh'
    test_xml = 'test_connect.xml'
    result_file = os.path.join('test_connect_result.txt')

    android_device_id = "R5CW51LN1PD"
    target_uuid = "0000180D-0000-1000-8000-00805f9b34fb"  # HR service UUID
    extra_address = "F1:CD:70:40:99:AA"  # MAC address of bluetooth device

    stdout, stderr = run_adb_test(
        android_device_id,
        target_uuid,
        extra_address,
        test_bat,
        test_xml,
        result_file,
    )
    print(stdout)
    print(stderr)

    result, message = check_test_results(result_file)
    print(result)
    print(message)
