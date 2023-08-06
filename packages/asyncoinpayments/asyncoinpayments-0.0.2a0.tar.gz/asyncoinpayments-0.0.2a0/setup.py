from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    
    long_description = "\n" + fh.read()

VERSION = '0.0.2a'
DESCRIPTION = 'Python Asynchronous Wrapper of the CoinPayments API'


# Setting up
setup(
    name="asyncoinpayments",
    version=VERSION,
    author="flalugli",
    author_email="<flalugli.dev@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/flalugli/asyncoinpayments",
    license="Apache License 2.0",
    packages=find_packages(),
    install_requires=['aiohttp', 'tenacity'],
    keywords=['python', 'crypto', 'cryptocurrency', 'payment gateway', 'async', 'aiohttp'],
    extras_require={"dev": ["twine>=4.0.2"]},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8"
)