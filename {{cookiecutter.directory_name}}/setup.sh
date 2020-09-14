#!/bin/bash

git init --template=template

python3 -m venv --prompt {{cookiecutter.project_slug}} .venv
source .venv/bin/activate
python setup.py build
python -m pip install -U pip
python -m pip install -U -e .

exit 0

# Vim: set ft=jinja.sh:
