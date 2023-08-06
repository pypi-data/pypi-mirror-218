import os
import pathlib
import json
import sys
import shutil
import pip._internal.req
from subprocess import run
from impose_cli.decorators import impose
from sydeploy.utils.simple import read_syd_yaml_file, get_full_path, run_function_if_valid_variables


AUTHENTICATION_MAPPING = {
    "build": {
        "codeartifact": "sydeploy.commands.authenticate.aws.authenticate_codeartifact_for_twine"
    },
    "download": {
        "codeartifact": "sydeploy.commands.authenticate.aws.authenticate_codeartifact_for_pip"
    }
}


@impose
def _settings():
    pass


def complete(package_directory: str = None):
    package_directory = get_full_path(package_directory)
    syd_contents = read_syd_yaml_file(package_directory, True)

    cleanup_function = clean_distribution
    if os.path.exists(os.path.join(package_directory, "setup.py")):
        delete_setup = False
    else:
        delete_setup = True
    try:
        # Step1, we clean the last run
        action = run_function_if_valid_variables(cleanup_function, locals(), syd_contents["meta"])

        # STEP 2, WE WANT TO AUTHENTICATE
        if "registry" not in syd_contents['meta']:
            raise "A registry must be defined for a Python package to be built"
        if syd_contents["meta"]["registry"] not in AUTHENTICATION_MAPPING["build"]:
            raise NotImplementedError(f"Authentication for {syd_contents['meta']} is not currently supported.")
        build_function_name = AUTHENTICATION_MAPPING["build"][syd_contents["meta"]["registry"]]
        action = run_function_if_valid_variables(build_function_name, locals(), syd_contents["meta"])

        # STEP 2, we want to build
        build_distribution_function = build_distribution
        action = run_function_if_valid_variables(build_distribution_function, locals(), syd_contents["meta"])

        # Step 3, we want to upload
        upload_distribution_function = upload_distribution
        action = run_function_if_valid_variables(upload_distribution_function, locals(), syd_contents["meta"])

    except Exception as e:
        print(str(e))

    finally:
        # Now we want to clean everything
        try:
            action = run_function_if_valid_variables(cleanup_function, locals(), syd_contents["meta"])
        except Exception as e:
            print(str(e))
            exit(0)


def build_distribution(package_directory: str, identifier: str, version: str):
    package_directory = get_full_path(package_directory)
    if os.path.exists(os.path.join(package_directory, "setup.py")):
        print("Setup.py file already exists.")
    else:
        # Step 1 is to build the setup.py file
        setup_contents = open(os.path.join(pathlib.Path(__file__).parent.parent.parent, "templates/setup.py.dist"), "r").read()
        # Let's find the requirements
        # The convention here is that everything is going to be a extra-requires beside internal
        main_requirements = []
        extra_requires = {}
        requirement_files = [file for file in os.listdir(package_directory) if os.path.isfile(os.path.join(package_directory, file)) and str(file).startswith("requirements")]
        for requirement_file in requirement_files:
            filename = str(requirement_file).replace(".txt", "")
            parts = filename.split(".")
            if len(parts) == 1:
                parts = filename.split("-")
            if len(parts) == 1:
                name = ""
            else:
                name = parts[1]
            requirement_temp = [str(ir.requirement) for ir in pip._internal.req.parse_requirements(os.path.abspath(os.path.join(package_directory, requirement_file)), session="build")]
            if name == "":
                main_requirements = requirement_temp
            else:
                extra_requires[name] = requirement_temp

        # Now we get the long description
        readme_files = [os.path.basename(file) for file in os.listdir(package_directory) if os.path.isfile(file) and str(os.path.basename(file)).startswith("README")]
        if len(readme_files) == 0:
            long_description = ""
        else:
            long_description = open(readme_files[0], "r").read()

        # Now we get the package_data
        result = [root for root, dirs, files in os.walk(os.path.join(package_directory, identifier)) if not any(file.endswith(".py") for file in files)]
        package_data = {identifier: ["{}/*".format(os.path.basename(x)) for x in result]}

        setup_contents = setup_contents.format(
            name=identifier,
            long_description=long_description,
            version=version,
            requirements=json.dumps(main_requirements),
            extra_requires=json.dumps(extra_requires),
            package_data=json.dumps(package_data)
        )
        open(os.path.join(package_directory, "setup.py"), "w").write(setup_contents)
    python_string = "python" + str(sys.version[0])
    print("Building the distribution now.")
    build_exec = run(args=f"{python_string} setup.py bdist_wheel", shell=True, cwd=package_directory, capture_output=True)
    # Check if it worked
    if not os.path.exists(os.path.join(package_directory, "dist")):
        raise "Building the distribution failed."

    print("The distribution has been built.")


def upload_distribution(package_directory: str, registry: str):
    package_directory = get_full_path(package_directory)
    config_path = "/tmp/.pypirc"
    if not os.path.exists("/tmp/.pypirc"):
        config_path = os.path.expanduser("~/.pypirc")

    upload_exec = run(args=f"twine upload --repository {registry} dist/* --config-file {config_path}", shell=True,
                      capture_output=True, cwd=package_directory)
    errors = upload_exec.stderr.decode("utf-8").strip()
    output = upload_exec.stdout.decode("utf-8").strip()
    if errors != "":
        raise Exception(errors)
    print("Finished uploading to artifact repo.")


@impose
def clean_distribution(package_directory: str = None, delete_setup: bool = True):
    package_directory = get_full_path(package_directory)

    if os.path.exists(os.path.join(package_directory, "setup.py")) and delete_setup:
        os.remove(os.path.join(package_directory, "setup.py"))
    deletion_directories = ["build", "dist"] + \
                           [file for file in os.listdir(package_directory)
                            if os.path.isdir(os.path.join(package_directory, file)) and str(file).endswith(".egg-info")]

    for directory in deletion_directories:
        if os.path.exists(os.path.join(package_directory, directory)):
            shutil.rmtree(os.path.join(package_directory, directory))
    print("Package directory is clean.")

