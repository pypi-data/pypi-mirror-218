import os
from setuptools import setup, find_packages
from pip._internal.req import parse_requirements


def find_package_data(package_directory):
    package_directory = os.path.join(os.path.dirname(__file__), package_directory)
    package_data = []
    for root, _, files in os.walk(package_directory):
        for file in files:
            package_data.append(os.path.relpath(os.path.join(root, file), package_directory))
    return package_data


setup(
    name='sydeploy',
    version='0.2.1rc9',
    license="LICENSE",
    packages=find_packages(include="syd_commands"),
    package_data={
        "syd": ["templates/*", "utils/*"] + find_package_data("syd/commands")
    },
    entry_points={
        'console_scripts': ['syd=syd.run:run']
    },
    install_requires=[str(ir.requirement) for ir in parse_requirements("requirements.txt", session='build')]
)
