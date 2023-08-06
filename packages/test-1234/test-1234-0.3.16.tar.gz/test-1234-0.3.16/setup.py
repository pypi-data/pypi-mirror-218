from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.3.16'
DESCRIPTION = 'A basic hello package'

# Setting up
setup(
    name="test-1234",
    version=VERSION,
    author="someone",
    author_email="<mail@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['setuptools'],
)
