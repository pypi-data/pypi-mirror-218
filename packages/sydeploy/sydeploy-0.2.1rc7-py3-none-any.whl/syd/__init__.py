import os
import importlib.util

directory_path = os.path.dirname(os.path.abspath(__file__))
python_files = [os.path.join(root, file) for root, _, files in os.walk(directory_path) for file in files if file.endswith(".py") and not file.endswith("__init__.py")]

for file in python_files:
    module_name = os.path.splitext(os.path.basename(file))[0]
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)