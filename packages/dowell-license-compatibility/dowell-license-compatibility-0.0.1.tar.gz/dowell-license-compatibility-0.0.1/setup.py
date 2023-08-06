from setuptools import setup, find_packages
import codecs
import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(BASE_PATH, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Open Source Licence Compatibility Check Package'

# Setting up
setup(
    name="dowell-license-compatibility",
    version=VERSION,
    author="Marvin Okwaro",
    author_email="<marvin.wekesa@gmal.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'License', 'Open Source', 'Compatibility'],
)