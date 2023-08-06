# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="pystax",
    version="0.2.0",
    description="pystax Python library",
    long_description="The pystax is a Python library that allows you to probe domains and IP addresses to check their status codes. It helps you verify the accessibility of a domain or IP by performing an HTTP request and retrieving the corresponding status code.,",
    long_description_content_type="text/markdown",
    author="Pritam Dash",
    author_email="pritamdash1997@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["pystax"],
    include_package_data=True
)