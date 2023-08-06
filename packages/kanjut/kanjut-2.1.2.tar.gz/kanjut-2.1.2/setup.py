import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as rd:
    long_description = rd.read()

setup(
    name="kanjut",
    version="2.1.2",
    author="Unknown",
    author_email="opetbae6@gmail.com",
    description="Client library for opet",
    url="https://github.com/opet321/nayu",
    license="AGPL",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['telethon', 'tgcrypto'],
    keywords=['pypi', 'mengontol', 'python', 'telethon', 'telebot'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
