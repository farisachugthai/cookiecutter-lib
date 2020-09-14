======
README
======

Cookiecutter for python libraries.

This is a substantially more fully featured cookiecutter than many other
popular cookiecutters.


Optional but complete library integration
=========================================

This python package does not force a user to use any particular set of tools,
IDEs, text editors, linting tools, formatters or libraries.

It does, however, come with complete and reasonable defaults if a user selects
certain options during repository creation.

For example, the :mod:`argparse` library in the Python Standard library is
very feature-complete; however, it requires a ton of boilerplate.

If the user chooses to use argparse, your source code will automatically
come with argparse integration, multiple option flags automatically provided,
and user specified :mod:`logging` through command line arguments.


Documentation
=============

The basic scaffolding for Sphinx documentation is greatly built upon.
Typically many cookiecutter projects won't enable necessary options that I use
in every single python project I use.

Specifically enabling helpful extensions and defaulting to ``py:obj`` as the
default Sphinx role are a few of the lengthy additions to the standard
`conf.py <./{{cookiecutter.directory_name}}/docs/conf.py>`_.


Unit Testing
=============

Local testing
-------------
Users can choose between unittest and pytest integration.

A `tox.ini <./{{cookiecutter.directory_name}}/tox.ini>`_ is also provided
for tox users. This comes with flake8 and sphinx integration as well as the
user supplied choice of pytest or unittest.

Travis
------

A travis YAML file is automatically generated to remotely run your
repositories source code.

GitHub
-------

In addition, GitHub issue templates are provided.



Linting
========

Configurations for flake8, pylint, and pydocstyle are set up automatically
in the ``setup.cfg`` file.

In addition, a large amount of standard metadata are automatically provided.
This requires a copy of setuptools more recent than version 30.0.3.


Additional Support for Tooling
==============================

There are abundant files provided to ease the typical drudgery of starting
a new project.


VSCode
------

Pytest or unittest is automatically enabled based on which one the user chooses
in initial setup.

