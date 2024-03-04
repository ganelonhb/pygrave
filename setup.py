""" Simple setup.py """

from os import path
from setuptools import setup

with open("README.md", "r") as f:
    DESCRIPTION=f.read()

setup(
    name="grave",
    version="0.0.1",
    python_requires=">=3.11.0",
    description="A modern game engine written in Python PyGame",
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=["grave"],
    author="Zachary Worcester",
    author_email="worcesterzj@gmail.com",
    install_requires=["pygame"],
    url="https://github.com/ganelonhb/pygrave",
    py_modules = ["testgrave"],
    package_data = {"invaderclone" : ["data/*", "data/themes/default/bgm/*", "data/themes/default/bgs/*", "data/themes/default/fonts/*", "data/themes/default/images/*"]},
    include_package_data=True,
    entry_points= {
        'console_scripts' : [
            'testgrave = testgrave:main'
            ]
        }
    )
