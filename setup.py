import os
import shutil
from setuptools import setup, find_packages


setup(
    name="pyfj",
    packages=find_packages(include=("pyfj",)),
    entry_points={"console_scripts": ["pyfj_cli = scripts.pyfj_cli:main"]},
    install_requires=["click"]
)

bin_dir = os.path.expanduser("~/.local/bin")
os.makedirs(bin_dir, exist_ok=True)
shutil.copy("fj.sh", bin_dir)
