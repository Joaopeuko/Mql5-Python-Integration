import json
import os
import pathlib

import setuptools

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name="mqpy",
    version="v0.6.0",
    description="",
    author="Joao Paulo Euko",
    license="MIT",
    keywords=["metatrader5", "algotrading", "stock market"],
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "python == ^3.8",
        "metatrader5 == ^5.0.45",
    ],
)
