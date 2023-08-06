from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

setup(
    name='sydeploy',
    version='0.2.2rc',
    license="LICENSE",
    install_requires=[str(ir.requirement) for ir in parse_requirements("requirements.txt", session='build')],
)