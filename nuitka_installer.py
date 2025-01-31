#!/usr/bin/python
import ast
import os
import subprocess
import sys


def resolve_sys_path_appends(file_path):
    """
    Extracts and resolves sys.path.append calls from the specified Python file.
    """
    with open(file_path, 'r') as f:
        source = f.read()
    tree = ast.parse(source, filename=file_path)
    file_dir = os.path.dirname(os.path.abspath(file_path))
    resolved_paths = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if (
            not isinstance(node.func.value, ast.Attribute) or
            node.func.value.attr != "path" or
            node.func.attr != "append"
        ):
            continue
        if len(node.args) != 1:
            continue
        arg = node.args[0]
        try:
            if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                left = eval(compile(ast.Expression(arg.left), filename="<ast>", mode="eval"),
                            {"__file__": file_path, 'os': os}, {})
                right = eval(compile(ast.Expression(arg.right), filename="<ast>", mode="eval"),
                             {"__file__": file_path, 'os': os}, {})
                resolved_path = os.path.normpath(os.path.join(file_dir, left + right))
            elif isinstance(arg, ast.Str):  # Direct string
                resolved_path = os.path.normpath(os.path.join(file_dir, arg.s))
            else:
                resolved_path = eval(compile(ast.Expression(arg), filename="<ast>", mode="eval"),
                                     {"__file__": file_path, 'os': os}, {})
            resolved_paths.append(resolved_path)
        except Exception as e:
            print(f"Could not resolve path for: {ast.dump(arg)} due to error: {e}")
    return resolved_paths

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <script_name.py> [additional pyinstaller arguments...]")
        sys.exit(1)
    script_name = sys.argv[1]
    additional_args = sys.argv[2:]
    # Resolve sys.path.append calls
    resolved_paths = resolve_sys_path_appends(script_name)
    # Build the pyinstaller command
    pyinstaller_command = ["nuitka"]
    pyinstaller_command.extend(additional_args)
    pyinstaller_command.append(script_name)
    # Print the command for debugging purposes
    print("Executing command:", " ".join(pyinstaller_command))
    env = os.environ.copy()
    env['PYTHONPATH'] = ':'.join([os.path.abspath(path) for path in resolved_paths])
    print('PYTHONPATH:', env["PYTHONPATH"])
    # Execute the pyinstaller command
    try:
        subprocess.run(pyinstaller_command, check=True, env=env)
    except subprocess.CalledProcessError as e:
        print("PyInstaller failed with error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
