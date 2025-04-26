# """Setup script for the mqpy package.

# This module contains the setup configuration for the mqpy package, which provides a Python interface
# for creating Expert Advisors in MetaTrader 5.
# """

from setuptools import find_packages, setup

setup(
    name="mqpy",
    version="0.6.9",
    packages=find_packages(),
    install_requires=[],
    author="Joao Euko",
    author_email="",
    description="A library to simplify creating Expert Advisors in MQL5",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    entry_points={
        "console_scripts": [
            "mqpy=mqpy.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
