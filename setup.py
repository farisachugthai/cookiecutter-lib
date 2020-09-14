# !/usr/bin/env python
from setuptools import setup

tests_requires = [
    "pytest",
    "pytest-cookies",
]

extras_requires = {
    "test": tests_requires
}

setup(
    name='cookiecutter-lib',
    packages=[],
    version='0.1.0',
    description='Cookiecutter template for a Python lib',
    author='Faris A Chugthai',
    license='MIT',
    author_email='farischugthai@gmail.com',
    url='https://github.com/farisachugthai/cookiecutter_lib',
    keywords=['cookiecutter', 'template', 'package', ],
    python_requires='>=3.5',
    install_requires=["cookiecutter"],
    tests_requires=tests_requires,
)
