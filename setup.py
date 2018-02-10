"""
Hack
----

Exposes a `hack` function to "hack open" an object from the Python Interpreter,
which loads the object's source file at the line its defined on using the
default or configured text editor.
"""

from distutils.sysconfig import get_python_lib
from distutils.core import setup


setup(
    name='hack-function',
    version='1.0.0',
    description='"Goto Definition" for the Python Interpreter.',
    long_description=__doc__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='https://github.com/joeyespo/hack-function',
    license='MIT',
    platforms='any',
    py_modules=['hack'],
    package_data={'': ['LICENSE']},
    data_files=[(get_python_lib(), ['hack_function_import_hook.pth'])],
)
