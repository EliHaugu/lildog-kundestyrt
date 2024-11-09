from urllib.parse import urlencode

import requests
from data_manager.models import Flow, Node
from django.shortcuts import get_object_or_404
from django.urls import reverse
from flow_parser import FlowParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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
                # TODO comment back in when this endpoint is implemented
                # res = self.check_device_connections(flow_id) T
                # if res['status'] != 'success':
                #     flow_result["status"] = "failed"
                #     flow_result["error"] = res["message"]
                #     results.append(flow_result)
                #     break

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
        protocol = 'https' if self.request.is_secure() else 'http'
        base_url = f"{protocol}://{self.request.get_host()}"
        check_devices_url = f"""
                            {base_url}{reverse('flow-device-connection')}
                            ?{urlencode({'flow_id': flow_id})}
                            """
        response = requests.get(check_devices_url)

        if response.status_code == 200:
            connection_data = response.json()
            if all(
                status['status'] == 'connected'
                for status in connection_data['response'].values()
            ):
                return {
                    "status": "success",
                    "message": "All devices connected",
                }
            else:
                return {
                    "status": "failed",
                    "message": "Some devices are not connected",
                    "details": connection_data['response'],
                }
        return {
            "status": "error",
            "message": "Failed to check device connections",
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
                # TODO add code from LIL-95
                result = True
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
