from os import getcwd
from os.path import expanduser, join, exists
from sydeploy.errors import MissingSCIDCConfig
from yaml import safe_load
from inspect import getfullargspec


def get_full_path(package_directory: str):
    if package_directory is None:
        return getcwd()
    if package_directory[0] == "~":
        package_directory = expanduser(package_directory)
    elif package_directory[0] != 0:
        package_directory = join(getcwd(), package_directory)
    return package_directory


def read_syd_yaml_file(package_directory: str, throw_error_on_missing: bool = True):
    syd_path = join(package_directory, "syd.yaml")
    if not exists(syd_path):
        if not throw_error_on_missing:
            return None
        else:
            raise MissingSCIDCConfig(package_directory)
    return safe_load(open(syd_path, "r"))


def run_function_if_valid_variables(function, local_variables: dict, syd_file_contents: dict):
    if isinstance(function, str):
        function_name = function.split(".")[-1]
        function_path = ".".join(function.split(".")[0:-1])
        try:
            global_namespace = {}
            exec(f"from {function_path} import {function_name}", global_namespace)
            if function_name in global_namespace and callable(global_namespace.get(function_name)):
                function = global_namespace[function_name]
        except:
            raise NotImplementedError(f"The function {function_name} does not exist.")
    passed_arguments = {}
    args = getfullargspec(function)
    if hasattr(args, "args"):
        args = args.args
    else:
        args = []
    for arg in args:
        if arg in local_variables:
            passed_arguments[arg] = local_variables[arg]
        elif arg in syd_file_contents:
            passed_arguments[arg] = syd_file_contents[arg]

    if len(passed_arguments) == len(args):
        return function(**passed_arguments)
    else:
        raise f"All arguments {', '.join(args)} are required in the syd.yaml file."



