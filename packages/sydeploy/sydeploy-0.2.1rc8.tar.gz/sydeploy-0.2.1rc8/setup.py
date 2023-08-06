from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

setup(
    name='sydeploy',
    version='0.2.1rc8',
    license="LICENSE",
    packages=find_packages(include="syd_commands"),
    package_data={
        "syd": ["templates/*", "utils/*"]
    },
    entry_points={
        'console_scripts': ['syd=syd.run:run']
    },
    install_requires=[str(ir.requirement) for ir in parse_requirements("requirements.txt", session='build')]
)
