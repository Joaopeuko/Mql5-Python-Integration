import json
import os
import pathlib

import setuptools

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()


def get_requirements_from_pipfile_lock(pipfile_lock=None):
    if pipfile_lock is None:
        pipfile_lock = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Pipfile.lock")
    lock_data = json.load(open(pipfile_lock))
    retval = []
    for package_name, package_data in lock_data.get("default", {}).items():
        if package_data.get("file"):
            package_ref = f'{package_name} @ {package_data["file"]}'
        else:
            package_ref = f'{package_name}{package_data["version"]}'
        retval.append(package_ref)
    return retval


def generate_requirements_txt(pipfile_lock_requirements):
    for requirement in pipfile_lock_requirements:
        with open(os.path.join("requirements.txt"), "w") as file:
            file.writelines(requirement)


requirements = get_requirements_from_pipfile_lock()
generate_requirements_txt(requirements)

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
