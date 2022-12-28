#!/usr/bin/env python
"""Setup config file."""

from os import path
from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tumblesac",
    version="1.0.2",
    packages=find_packages(),
    install_requires=["numpy==1.23.4", "pygame==2.1.2", "requests=2.26.0"],
    author="Antoine Pirrone",
    author_email="antoine.pirrone@gmail.com",
    url="https://github.com/apirrone/TUMBLESAC",
    description="Rewriting tumblestone to play it online with my friends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "tumblesac = tumblesac.__main__:main",
            "tumblesac_server = tumblesac.server.__main__:main",
        ]
    },
)
