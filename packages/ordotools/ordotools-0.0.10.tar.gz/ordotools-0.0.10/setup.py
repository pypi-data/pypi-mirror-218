from setuptools import find_packages
from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ordotools",
    version="0.0.10",
    description="A set of tools for producing a traditional Catholic Ordo, given a year and diocese",
    # package_dir={"": "ordotools"},
    # packages=find_packages(where="ordotools"),
    packages=["ordotools"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/corei8/ordotools",
    author="corei8 (Fr. G.R.Barnes)",
    author_email="corei8.github@gmail.com",
    license="GNU",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        "python-dateutil"
    ],
    python_requires=">=3.7",
)

