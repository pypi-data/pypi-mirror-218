from setuptools import setup, find_packages

setup(
    name='sydeploy',
    version='0.2.1rc11',
    license="LICENSE",
    packages=find_packages(include=["commands", "commands.*"]),
    package_data={
        "syd": ["command/*", "templates/*", "utils/*"]
    },
    entry_points={
        'console_scripts': ['syd=syd.run:run']
    },
    install_requires=['requirements'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)