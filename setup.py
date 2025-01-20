import pathlib

import setuptools

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name="mqpy",
    version="v0.6.9",
    description="I developed this library to simplify the process of creating an Expert Advisor in MQL5. While developing in MQL5 can be complex, the same task is more streamlined in Python.",
    author="Joao Paulo Euko",
    license="MIT",
    keywords=["metatrader5", "algotrading", "stock market"],
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "metatrader5 == 5.0.4803",
        "setuptools == 75.8.0",
    ],
    entry_points={
        "console_scripts": [
            "mqpy = __main__:main",
        ],
    },
)
