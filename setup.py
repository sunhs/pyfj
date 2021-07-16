import os
import shutil
from setuptools import setup, find_packages


setup(
    name="pyfj", packages=find_packages(include=("pyfj",)), scripts=["scripts/pyfj_cli.py"], install_requires=["click"]
)

bin_dir = os.path.expanduser("~/.local/bin")
os.makedirs(bin_dir, exist_ok=True)
shutil.copy("fj.sh", bin_dir)
