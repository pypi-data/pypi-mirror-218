from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

setup(
    name='sydeploy',
    version='0.2.1rc12',
    license="LICENSE",
    packages=find_packages(include=["commands", "commands.*"]),
    package_data={
        "syd": ["command/*", "templates/*", "utils/*"]
    },
    entry_points={
        'console_scripts': ['syd=syd.run:run']
    },
    install_requires=[str(ir.requirement) for ir in parse_requirements("requirements.txt", session='build')],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)