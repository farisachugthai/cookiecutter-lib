#!/usr/bin/env python
"""The setup script."""
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

{#
For some reason these 2 parts aren't working at ALL

requirements = [
    {%- if cookiecutter.command_line_interface|lower == 'click' % }'Click>=7.0', {%- endif %}
]

test_requirements = [
    {%- if cookiecutter.use_pytest == 'y' % }'pytest>=3', {%- endif%}
]

This works but I removed it. Keep note of this though! It would be nice to have a template
file or something where we can set this variable in basically any jinja template I need
to in the repository.
#}

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    description="{{ cookiecutter.project_short_description }}",
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.core:main',
        ],
    },
    {%- endif %}
    {# install_requires=requirements, #}
    license="{{ cookiecutter.open_source_license }}",
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(
        include=[
        '{{ cookiecutter.project_slug }}', '{{ cookiecutter.project_slug }}.*'
    ]),
    test_suite='tests',
    {# tests_require=test_requirements,#}
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    zip_safe=False,
)

# Vim: set ft=jinja:python:
