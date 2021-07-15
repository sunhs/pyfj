from setuptools import setup, find_packages


setup(name="pyfj", packages=find_packages(include=("pyfj",)), scripts=["scripts/cli.py"], install_requires=["click"])
