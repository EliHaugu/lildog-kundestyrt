import ast


class node_checker:

    @staticmethod
    def check_valid_input(function: str) -> bool:
        try:
            tree = ast.parse(function)
        except SyntaxError:
            raise ValueError("Input is not correct syntax for Python.")

        for node in ast.walk(tree):
            if isinstance(node, ast.Return):
                if isinstance(node.value, ast.Constant) and isinstance(
                    node.value.value, bool
                ):
                    return True

        raise ValueError(
            "Input does not contain a return statement with a boolean value."
        )