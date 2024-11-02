from . import logic
from data_manager.models import Node
from django.forms import ValidationError
from django.http import HttpResponseBadRequest, JsonResponse


async def check_assertion_view(request, node_id):
    if request.method == "POST":
        node = Node.objects.filter(id=node_id, node_type=Node.ASSERT).first()
        if not node:
            return HttpResponseBadRequest("Invalid node.")

        try:
            if node.assertion_method == Node.API:
                result = logic.check_api_assertion(node)
                return JsonResponse({"result": result})

            elif node.assertion_method == Node.UART:
                uart_log_file_path = request.POST.get("uart_log_file_path")
                if not uart_log_file_path:
                    return JsonResponse(
                        {"result": "Missing UART log file path."}, status=400
                    )

                result = logic.check_uart_assertion(node, uart_log_file_path)
                return JsonResponse({"result": result})
            else:
                return JsonResponse(
                    {"result": "Unsupported assertion method."}, status=400
                )

        except ValidationError as e:
            return JsonResponse(
                {"result": "Assertion Error", "error": str(e)}, status=400
            )
    return HttpResponseBadRequest("Invalid request method.")

    # UART assertion for async fetching of UART logs


#            elif node.assertion_method == Node.UART:
#               # Assuming uart_reader is set up to read UART data
#                uart_reader = await create_uart_stream_reader()
#                result = await logic.check_uart_assertion(node, uart_reader)
#                return JsonResponse({"result": result})
#            else:
#                return JsonResponse({"result": "Unsupported assertion method."
#                }, status=400)
