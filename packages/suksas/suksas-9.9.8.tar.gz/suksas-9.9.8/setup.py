import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as rd:
    long_description = rd.read()

setup(
    name="suksas",
    version="9.9.8",
    author="Unknown",
    author_email="iyakenapa41@gmail.com",
    description="Client library for mengontol",
    url="https://github.com/kastaid/pytelibs",
    license="AGPL",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pyrogram', 'tgcrypto'],
    keywords=['pypi', 'mengontol', 'python', 'pyrogram', 'telebot'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
