# !/usr/bin/env python
from setuptools import setup

install_requires = [
    "cookiecutter",
    "PyYaml>=*",
]

tests_requires = [
    "pytest",
    "pytest-cookies",
]

docs_requires = [
    "sphinx",
]

extras_requires = {
    "test": tests_requires,
    "docs": docs_requires,
    "dev": tests_requires+docs_requires,
}

setup(
    author='Faris A Chugthai',
    author_email='farischugthai@gmail.com',
    description='Cookiecutter template for a Python lib',
    extras_requires=extras_requires,
    install_requires=install_requires,
    keywords=['cookiecutter', 'template', 'package', ],
    license='MIT',
    name='cookiecutter-lib',
    packages=[],
    python_requires='>=3.5',
    tests_requires=tests_requires,
    url='https://github.com/farisachugthai/cookiecutter_lib',
    version='0.2.0',
)
