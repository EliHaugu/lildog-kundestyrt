import json

from data_manager.models import Flow, Node
from device_connection.views import FlowDeviceConnectionView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from flow_parser import FlowParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from test_runner.default_nodes import run_default_node


class RunTestFlow(APIView):
    """
    API endpoint to run a specific test flow by flow_id
    or all test flows if no flow_id is specified.
    """

    def post(self, request, flow_id=None):
        if flow_id:
            flow = get_object_or_404(Flow, id=flow_id)
            test_flows = [flow]
        else:
            # Run all test flows if no flow_id is specified
            test_flows = Flow.objects.all()

        results = []

        for flow in test_flows:
            flow_id = flow.id
            flow_result = {
                "flow_name": flow.name,
                "nodes_executed": [],
                "status": "success",
                "error": None,
            }
            try:
                res = self.check_device_connections(flow_id)
                if res['status'] != 'success':
                    flow_result["status"] = "failed"
                    flow_result["error"] = res["message"]
                    results.append(flow_result)
                    break

                flow_parser = FlowParser(flow)
                execution_order = flow_parser.get_execution_order()

                for parallel_nodes in execution_order:
                    for node in parallel_nodes:

                        result = self.run_node(node)
                        flow_result["nodes_executed"].append(result)

                        if result["status"] == "failed":
                            flow_result["status"] = "failed"
                            flow_result["error"] = result["error"]
                            results.append(flow_result)
                            break

            except Exception as e:
                flow_result["status"] = "failed"
                flow_result["error"] = str(e)

            results.append(flow_result)

        return Response({"results": results}, status=status.HTTP_200_OK)

    def check_device_connections(self, flow_id):
        """
        Checks device connectivity for the flow.
        """

        device_manager = FlowDeviceConnectionView()
        responses = device_manager.connect_devices(flow_id)

        if not responses:
            return {
                "status": "error",
                "message": "Failed to check device connections",
            }

        parsed_responses = []
        for response in responses:
            if isinstance(response, JsonResponse):
                response_content = response.content.decode('utf-8')
                response_json = json.loads(response_content)
                parsed_responses.append(response_json['response'])
            elif isinstance(response, bytes):
                response_str = response.decode('utf-8')
                response_json = json.loads(response_str)
                for res in response_json['response']:
                    parsed_responses.append(res)
            else:
                parsed_responses.append(response)

        if all(
            response.get('status') == 'connected'
            for response in parsed_responses
        ):
            return {
                "status": "success",
                "message": "All devices connected",
            }
        else:
            return {
                "status": "failed",
                "message": (
                    f"Some devices are not connected: {parsed_responses}"
                ),
            }

    def run_node(self, node):
        """
        Execute a single node's function and return the result.
        """
        try:
            result = None
            if node.node_type == Node.ASSERT:

                result = self.check_assertion(node.function)

            elif node.node_type == Node.ACTION:
                try:
                    function = node.function.split("\n")
                    if (
                        len(function) > 1
                        and "THIS IS A DEFAULT NODE" in function[1]
                    ):
                        res = json.loads(run_default_node(node).content)
                        if res['status'] != "success":
                            return {
                                "node_id": node.id,
                                "status": "failed",
                                "output": res,
                            }
                    else:
                        exec(node.function)
                    result = True
                except Exception as e:
                    ex_type = type(e).__name__
                    raise ValueError(f"Invalid Python code, {ex_type}:{e}")
            else:
                raise ValueError(f"Invalid node type: {node.node_type}")
            return {
                "node_id": node.id,
                "status": "success",
                "output": result,
            }
        except Exception as e:
            return {
                "node_id": node.id,
                "status": "failed",
                "error": str(e),
            }

    def check_assertion(self, function):
        """
        Executes a given function and checks if it returns a boolean value.
        Raises:
        ValueError: If the executed function does not return a boolean value.
        """
        function_code = "def temp_function():\n    " + function.replace(
            "\n", "\n    "
        )
        local_scope = {}
        exec(function_code, {}, local_scope)

        result = local_scope['temp_function']()

        if not isinstance(result, bool):
            raise ValueError("The function did not return a boolean value.")

        return result
