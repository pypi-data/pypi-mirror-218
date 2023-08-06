from os import getcwd
from os.path import expanduser, join, exists
from sydeploy.errors import MissingSCIDCConfig
from yaml import safe_load


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
