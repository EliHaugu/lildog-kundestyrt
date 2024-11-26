import ast
import json
import os

from data_manager.models import Category, Device, Node
from django.http import JsonResponse
from test_runner.nrf_scripts.nrf_connect import (
    run_check_connection,
    run_custom_script,
)


def run_default_node(node: Node):
    function = node.function.split("\n")[0]
    node_type = function.split("TYPE: ")[1].split(",")[0].strip()

    match node_type.lower():
        case "nrf connect":
            return run_nrf_connect_node(node)
        case "nrf custom":
            return run_nrf_custom_node(node)
        case _:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "no such default node type",
                    "response": None,
                }
            )


def run_nrf_connect_node(node: Node):
    device: Device = node.device  # type: ignore
    category: Category = device.category  # type: ignore
    connection_types = category.connection_types
    connection_ids = device.connection_ids

    if "adb" not in connection_types:
        return JsonResponse(
            {
                "status": "error",
                "message": "device is not adb category device",
                "response": None,
            }
        )

    if "adb_device_id" not in connection_ids.keys():
        return JsonResponse(
            {
                "status": "error",
                "message": "device lacks adb device id",
                "response": None,
            }
        )

    adb_device_id = connection_ids['adb_device_id']
    function = node.function

    try:
        mac_adr_string = function.split("mac_addresses = ")[1].strip()
        mac_adr_list = ast.literal_eval(mac_adr_string)
        mac_adr_list = [mac_adr.strip() for mac_adr in mac_adr_list]
    except Exception as e:
        return JsonResponse(
            {
                "status": "error",
                "message": (
                    "wrong nrf connect node format, couldn't get mac addresses"
                ),
                "response": str(e),
            }
        )

    results = []
    for mac_adr in mac_adr_list:
        res = json.loads(
            run_check_connection(adb_device_id, mac_adr).content.decode(
                'utf-8'
            )
        )
        results.append(res)

    if all(res['status'] == 'success' for res in results):
        return JsonResponse(
            {
                "status": "success",
                "message": "succeeded connecting to all nRF devices",
                "response": results,
            }
        )
    return JsonResponse(
        {
            "status": "error",
            "message": "some nRF devices failed to connect",
            "response": results,
        }
    )


def run_nrf_custom_node(node: Node):
    device: Device = node.device  # type: ignore
    category: Category = device.category  # type: ignore
    connection_types = category.connection_types
    connection_ids = device.connection_ids

    if "adb" not in connection_types:
        return JsonResponse(
            {
                "status": "error",
                "message": "device is not adb category device",
                "response": None,
            }
        )

    if "adb_device_id" not in connection_ids.keys():
        return JsonResponse(
            {
                "status": "error",
                "message": "device lacks adb device id",
                "response": None,
            }
        )

    adb_device_id = connection_ids['adb_device_id']
    function = node.function

    # try to get variables for script from function
    try:
        variables_str = function.split("# VARIABLES START")[1].split(
            "# VARIABLES END"
        )[0]
        variables_dict = ast.literal_eval(variables_str)
    except Exception as e:
        return JsonResponse(
            {
                "status": "error",
                "message": (
                    "wrong nrf custom node format, couldn't get variables"
                ),
                "response": str(e),
            }
        )

    # try to write custom xml script to file
    try:
        xml_script = (
            function.split("# XML SCRIPT START")[1]
            .split("# XML SCRIPT END")[0]
            .strip()
        )

        script_dir = os.path.dirname(__file__)
        os.chdir(script_dir)

        with open("./nrf_scripts/custom_script.xml", "w") as file:
            file.write(xml_script)
    except Exception as e:
        return JsonResponse(
            {
                "status": "error",
                "message": (
                    "wrong nrf custom node format, couldn't get xml script"
                ),
                "response": str(e),
            }
        )

    return run_custom_script(adb_device_id, variables_dict)
