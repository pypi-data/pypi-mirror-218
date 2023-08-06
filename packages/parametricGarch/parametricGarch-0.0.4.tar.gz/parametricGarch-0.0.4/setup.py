# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

LONG_DESCRIPTION = long_description

# This call to setup() does all the work
setup(
    name="parametricGarch",
    version="0.0.4",
    description="Parametric Bootstrapping via the GARCH model",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/chideraani/ParametricGarch",
    author="Chidera",
    author_email="chideraani27@gmail.com",
    license="GNU",
    keywords=['python', 'bootstrapping', 'garch', 'volatility', 'VaR', 'risk management', 'parametric bootstrapping'],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["parametricGarch"],
    include_package_data=True,
    install_requires=["numpy", "arch", "pandas", "scipy"]
)