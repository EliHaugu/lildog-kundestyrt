import datetime

import requests
from django.forms import ValidationError


def check_api_assertion(node):
    try:
        response = requests.post(node.api_url, json=node.api_payload)
        response_data = response.json()

        if response_data == node.expected_response:
            return "Assert OK"
        else:
            return "Assert Failed"
    except requests.exceptions.RequestException as e:
        raise ValidationError(f"API request failed: {e}")
    except ValueError:
        raise ValidationError("Expected a JSON response from the API.")


def check_uart_assertion(node, uart_log_file_path):
    start_time = datetime.now()

    try:
        with open(uart_log_file_path, 'r') as file:
            for line in file:
                if (
                    datetime.now() - start_time
                ).total_seconds() > node.timeout:
                    return "Assert Failed"

                if node.expected_uart_log in line:
                    return "Assert OK"

    except FileNotFoundError:
        return "Log file not found"
    except Exception as e:
        return f"Error reading log file: {str(e)}"

    return "Assert Failed"


# async def check_uart_assertion(node, uart_reader):
#    start_time = datetime.now()
#    while (datetime.now() - start_time).total_seconds() < node.timeout:
#       uart_line = await uart_reader.readline()
#       uart_line = uart_line.decode('utf-8')
#       if node.expected_uart_log in uart_line:
#            return "Assert OK"
#    return "Assert Failed"
