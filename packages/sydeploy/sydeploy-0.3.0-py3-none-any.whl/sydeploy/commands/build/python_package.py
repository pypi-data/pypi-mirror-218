import sys
import os
import shutil
import importlib
import json
from impose_cli.decorators import impose
from yaml import safe_load
from os import listdir
from pip._internal.req import parse_requirements
from subprocess import run
from os.path import join, exists, basename, dirname, abspath, isdir
from inspect import getfullargspec
from sydeploy.utils.simple import get_full_path


FLOW = ["bundle", "sydeploy.commands.authenticate.{registry}", "upload", "cleanup"]


@impose
def from_config_file(package_directory: str = None):
    package_directory = get_full_path(package_directory)
    if not exists(join(package_directory, "syd.yaml")):
        raise FileNotFoundError("For build to be automated using the from-config-file command, "
                                "the meta.yaml file must be configured.")
    meta = safe_load(open(join(package_directory, "syd.yaml"), "r"))
    for step in FLOW:
        for key, value in meta["syd"].items():
            key = f"{{{key}}}".lower()
            if key in step:
                step = step.replace(key, value.lower())
        step = step.replace("-", "_")
        function = None
        true_condition = False
        if step in globals() and callable(globals()[step]):
            true_condition = True
            function = globals()[step]
        else:
            try:
                module = importlib.import_module(step, package="sydeploy")
                features = dir(module)
                if "twine" in features and callable(getattr(module, "twine")):
                    true_condition = True
                    function = getattr(module, "twine")
            except Exception as e:
                print("No module found.")
        if true_condition:
            provided_args = {}
            args = getfullargspec(function)
            # There are two cases: if the argument was provided to this function, or if the argument is in the file
            for arg in args.args:
                if arg in meta["syd"]:
                    provided_args[arg] = meta["syd"][arg]
                if arg in locals() and not callable(locals()[arg]):
                    provided_args[arg] = locals()[arg]
            function(**provided_args)

@impose
def bundle(package_directory: str = None, version: str = None):
    if version is None:
        raise Exception("A package directory and version must be defined.")
    python_type = f"python{sys.version_info[0]}"
    print(f"The correct python alias is {python_type}.")

    package_directory = get_full_path(package_directory)
    package_name = basename(package_directory)
    if exists(join(package_directory, "README.rst")):
        long_description = open(join(package_directory, "README.rst"), "r").read()
    else:
        print("No README was found for the package -- the description will be empty.")
        long_description = ""

    setup_file = open(join(dirname(abspath(__file__)), "../templates/setup.py.dist"), "r").read()
    requirements_path = join(package_directory, "requirements.txt")
    requirements = [] if not exists(requirements_path) \
        else [str(ir.requirement) for ir in parse_requirements(requirements_path, session='build')]
    requirements = "[{}]".format(', '.join(f'"{s}"' for s in requirements))

    # Now we look for directories within the package directory and include them in the package data
    directories = listdir(join(package_directory, package_name))
    directories = ["{}/*".format(x) for x in directories if x[0] != "." and isdir(join(package_directory, "{}/{}".format(package_name, x)))]
    package_data = json.dumps({package_name: directories}) if len(directories) > 0 else json.dumps({})

    setup_file = setup_file.format(
        name=package_name,
        long_description=long_description,
        version=version,
        requirements=requirements,
        package_data=package_data
    )

    print("Finished formatting the setup.py file.")
    open(join(package_directory, "setup.py"), "w").write(setup_file)

    # Now we build the wheel file
    run(args=f"{python_type} setup.py bdist_wheel", shell=True, cwd=package_directory)
    print("The distribution has been built.")


@impose
def upload(package_directory: str = None, host: str = None):
    if host is None:
        raise Exception("A pypi host must be defined.")
    command = f"twine upload --repository {host.lower()} dist/*"
    run(args=command, cwd=package_directory, shell=True)

@impose
def cleanup(package_directory: str = None):
    package_directory = get_full_path(package_directory)

    package_name = basename(package_directory)
    if exists(join(package_directory, "setup.py")):
        os.remove(join(package_directory, "setup.py"))
    for directory in ["build", f"{package_name}.egg-info", "dist"]:
        if exists(join(package_directory, directory)):
            shutil.rmtree(join(package_directory, directory))
    print("Package directory is clean.")