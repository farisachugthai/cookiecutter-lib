#!/usr/bin/env python
import os
import shlex
import subprocess
from contextlib import contextmanager
# from shutil import rmtree


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
    # try:
    yield result
    # finally:
    #     rmtree(str(result.project))


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None


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
