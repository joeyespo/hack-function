"""
Hack
----

Exposes a `hack` function to "hack open" an object from the Python
Interpreter, which loads the object's source file at the line its
defined on using the default or configured text editor. It can also
print out or return a string of this metadata instead.
"""

from distutils.command.build import build
from os.path import dirname, join
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.easy_install import easy_install
from setuptools.command.install_lib import install_lib


PTH_FILE = 'hack_function.pth'


def make_command(base, command_dir='install_dir'):
    class CommandWithPth(base):
        def run(self):
            base.run(self)
            src = join(dirname(__file__), PTH_FILE)
            dest = join(getattr(self, command_dir), PTH_FILE)
            self.copy_file(src, dest)
            self._outputs = [dest]

        def get_outputs(self):
            return list(base.get_outputs(self)) + self._outputs

    return CommandWithPth


setup(
    name='hack-function',
    version='1.1.0',
    description='"Goto Definition" for the Python Interpreter.',
    long_description=__doc__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='https://github.com/joeyespo/hack-function',
    license='MIT',
    platforms='any',
    py_modules=['hack_function'],
    zip_safe=False,
    cmdclass={
        'build': make_command(build, 'build_lib'),
        'easy_install': make_command(easy_install),
        'install_lib': make_command(install_lib),
        'develop': make_command(develop),
    },
)
