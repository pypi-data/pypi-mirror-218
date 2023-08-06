from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

setup(
    name='sicdeploy',
    version='0.2.1rc',
    license="LICENSE",
    packages=find_packages(),
    package_data={
        "sicdeploy": ["commands/*", "templates/*"]
    },
    entry_points={
        'console_scripts': ['sicd=sicd.run:run']
    },
    install_requires=[str(ir.requirement) for ir in parse_requirements("requirements.txt", session='build')]
)
