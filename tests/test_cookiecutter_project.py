#!/usr/bin/env python
"""Note that the whole thing fails if run in the tests dir.

.. warning::

    Must be run in root of repo.

"""
import datetime
import logging
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager
from shutil import rmtree
from importlib.util import spec_from_file_location, module_from_spec

import yaml

from click.testing import CliRunner


logging.basicConfig(level=logging.WARNING)


@contextmanager
def inside_dir(dirpath):
    """Execute code from inside the given directory.

    :param dirpath: Path of the directory the command is being run.
    :type dirpath: str
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """Delete the temporal directory that is created when executing the tests.

    :param cookies: Cookie to be baked and its temporal files will be removed.
    :type cookies: pytest_cookies.Cookies
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        try:
            rmtree(str(result.project))
        except FileNotFoundError:
            pass


def run_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the exit status

    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        # assert result.exception is None
        if result.exception is not None:
            logging.exception(result.exception)


def test_bake_produced_correct_files(cookies):
    with bake_in_temp_dir(cookies) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'setup.py' in found_toplevel_files
        assert 'boilerplate' in found_toplevel_files
        assert 'tox.ini' in found_toplevel_files
        assert 'tests' in found_toplevel_files


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir('python setup.py test', str(result.project)) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    with bake_in_temp_dir(
        cookies,
        extra_context={'full_name': 'name "quote" name'}
    ) as result:
        assert result.project.isdir()
        run_inside_dir('python setup.py test', str(result.project)) == 0


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join('LICENSE')
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break setup.py"""
    with bake_in_temp_dir(
        cookies,
        extra_context={'full_name': "O'connor"}
    ) as result:
        assert result.project.isdir()
        run_inside_dir('python setup.py test', str(result.project)) == 0


def test_bake_without_travis_pypi_setup(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={'use_pypi_deployment_with_travis': 'n'}
    ) as result:
        with open(result.project.join(".travis.yml")) as f:
            travis_yaml = f.read()
        result_travis_config = yaml.load(
            travis_yaml,
            Loader=yaml.FullLoader
        )
        assert "deploy" not in result_travis_config
        assert "python" == result_travis_config["language"]
        # found_toplevel_files = [f.basename for f in result.project.listdir()]


def test_bake_without_author_file(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={'create_author_file': 'n'}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'AUTHORS.rst' not in found_toplevel_files
        doc_files = [f.basename for f in result.project.join('docs').listdir()]
        assert 'authors.rst' not in doc_files

        # Assert there are no spaces in the toc tree
        docs_index_path = result.project.join('docs/index.rst')
        with open(str(docs_index_path)) as index_file:
            assert 'contributing\n   history' in index_file.read()

        # Check that
        manifest_path = result.project.join('MANIFEST.in')
        with open(str(manifest_path)) as manifest_file:
            assert 'AUTHORS.rst' not in manifest_file.read()


def test_make_help(cookies):
    with bake_in_temp_dir(cookies) as result:
        # The supplied Makefile does not support win32
        if sys.platform != "win32":
            output = check_output_inside_dir(
                'make help',
                str(result.project)
            )
            assert b"check code coverage quickly with the default Python" in output


def test_bake_selecting_license(cookies):
    license_strings = {
        'MIT license': 'MIT ',
        'BSD license': 'Redistributions of source code must retain the ' +
                       'above copyright notice, this',
        'ISC license': 'ISC License',
        'Apache Software License 2.0':
            'Licensed under the Apache License, Version 2.0',
        'GNU General Public License v3': 'GNU GENERAL PUBLIC LICENSE',
    }
    for license, target_string in license_strings.items():
        with bake_in_temp_dir(
            cookies,
            extra_context={'open_source_license': license}
        ) as result:
            assert target_string in result.project.join('LICENSE').read()
            assert license in result.project.join('setup.py').read()


# Uh TODO:
# def test_using_pytest(cookies):
#     with bake_in_temp_dir(
#         cookies,
#         extra_context={'use_pytest': 'y'}
#     ) as result:
#         assert result.project.isdir()
#         test_file_path = result.project.join(
#             'tests/test_cookiecutter_project.py'
#         )
#         lines = test_file_path.readlines()
#         assert "import pytest" in ''.join(lines)
#         # Test the new pytest target
#         run_inside_dir('python setup.py pytest', str(result.project)) == 0
#         # Test the test alias (which invokes pytest)
#         run_inside_dir('python setup.py test', str(result.project)) == 0


# def test_not_using_pytest(cookies):
#     with bake_in_temp_dir(cookies) as result:
#         assert result.project.isdir()
#         test_file_path = result.project.join(
#             'tests/test_cookiecutter_project.py'
#         )
#         lines = test_file_path.readlines()
#         assert "import unittest" in ''.join(lines)
#         assert "import pytest" not in ''.join(lines)


def test_bake_with_no_console_script(cookies):
    context = {'command_line_interface': "No command-line interface"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" not in found_project_files

    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' not in setup_file.read()


def test_bake_with_console_script_files(cookies):
    context = {'command_line_interface': 'click'}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "core.py" in found_project_files

    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' in setup_file.read()


def test_bake_with_argparse_console_script_files(cookies):
    context = {'command_line_interface': 'argparse'}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "core.py" in found_project_files

    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' in setup_file.read()


# More todo
# def test_bake_with_console_script_cli(cookies):
#     context = {'command_line_interface': 'click'}
#     result = cookies.bake(extra_context=context)
#     project_path, project_slug, project_dir = project_info(result)
#     module_path = os.path.join(project_dir, 'core.py')
#     module_name = '.'.join([project_slug, 'core'])
#     spec = spec_from_file_location(module_name, module_path)
#     cli = module_from_spec(spec)
#     spec.loader.exec_module(cli)
#     runner = CliRunner()
#     noarg_result = runner.invoke(cli.main)
#     assert noarg_result.exit_code == 0
#     noarg_output = ' '.join([
#         'Replace this message by putting your code into',
#         project_slug])
#     assert noarg_output in noarg_result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert 'Show this message' in help_result.output


# def test_bake_with_argparse_console_script_cli(cookies):
#     context = {'command_line_interface': 'argparse'}
#     result = cookies.bake(extra_context=context)
#     project_path, project_slug, project_dir = project_info(result)
#     module_path = os.path.join(project_dir, 'core.py')
#     module_name = '.'.join([project_slug, 'core'])
#     spec = spec_from_file_location(module_name, module_path)
#     cli = module_from_spec(spec)
#     spec.loader.exec_module(cli)
#     runner = CliRunner()
#     noarg_result = runner.invoke(cli.main)
#     assert noarg_result.exit_code == 0
#     noarg_output = ' '.join([
#         'Replace this message by putting your code into',
#         project_slug])
#     assert noarg_output in noarg_result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert 'Show this message' in help_result.output


if __name__ == "__main__":
    import pytest
    pytest.main()
