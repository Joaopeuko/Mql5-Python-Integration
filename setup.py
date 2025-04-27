"""Setup script for the mqpy package.

This module contains the setup configuration for the mqpy package, which provides a Python interface
for creating Expert Advisors in MetaTrader 5.
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read the README for the long description
with Path("README.md").open(encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mqpy",
    version="0.6.9",
    packages=find_packages(),
    install_requires=[],
    author="Joao Euko",
    author_email="",
    description="A library to simplify creating Expert Advisors in MQL5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    entry_points={
        "console_scripts": [
            "mqpy=mqpy.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
