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
    name="EmailXtract",
    version="1.0.0",
    description="EmailXtract is a Python library that allows you to scrape email addresses from web pages",
    long_description="EmailXtract is a Python library that allows you to scrape email addresses from web pages within "
                     "a given domain. It provides a simple and convenient way to extract email addresses from "
                     "websites, making it useful for tasks such as email list building, contact information "
                     "gathering, and data analysis.",
    long_description_content_type="text/markdown",
    author="Pritam Dash",
    author_email="pritamdash1997@gmail.com.com",
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
    packages=["emailxtract"],
    include_package_data=True,
    install_requires=["requests", "beautifulsoup4", ]
)