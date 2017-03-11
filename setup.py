"""
Provides project-level commands. Commands are run via `python setup.py <command> [args]`

Commands available:
 - none
"""

from setuptools import setup, Command

import os


class RunInRootCommand(Command):
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        self.runcmd()

    def runcmd(self):
        pass


class ApiDocCommand(RunInRootCommand):
    description = "regenerates the API docs"

    def runcmd(self):
        os.system('"sphinx-apidoc" -f -e -o docs/apidoc .')


class AutoBuildCommand(RunInRootCommand):
    description = "watches the docs for changes and rebuilds them, automatically refreshing the browser page"

    def runcmd(self):
        os.system("sphinx-autobuild docs docs/_build/html -B")


setup(
    name='pyhamcrest-mock',
    version='0.0.1',
    description='Adds mock matchers to pyhamcrest.',
    url='',
    author='mdma',
    author_email='',
    license='Apache 2.0',
    package_dir={'': 'src'},
    packages=['pyhamcrest.mock'],
    zip_safe=False,
    cmdclass={
        'apidoc': ApiDocCommand,
        'autobuild': AutoBuildCommand
    }
)
