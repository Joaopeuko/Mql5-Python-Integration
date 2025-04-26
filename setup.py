"""Setup script for the mqpy package.

This module contains the setup configuration for the mqpy package, which provides a Python interface
for creating Expert Advisors in MetaTrader 5.
"""

import pathlib

import setuptools

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name="mqpy",
    version="v0.6.9",
    description=(
        "A library to simplify the process of creating an Expert Advisor in MQL5. "
        "It makes Python development more streamlined than MQL5."
    ),
    author="Joao Paulo Euko",
    license="MIT",
    keywords=["metatrader5", "algotrading", "stock market"],
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "metatrader5 == 5.0.4874",
        "setuptools == 78.1.0",
    ],
    entry_points={
        "console_scripts": [
            "mqpy = __main__:main",
        ],
    },
)
