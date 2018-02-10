Hack - "Goto Definition" for the Python Interpreter
===================================================

[![Current version on PyPI](http://img.shields.io/pypi/v/hack-function.svg)](http://pypi.python.org/pypi/hack-function/)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-😊-1EAEDB.svg)](https://saythanks.io/to/joeyespo)

Exposes a `hack` function to "hack open" an object from the Python Interpreter,
which loads the object's source file at the line its defined on using the
default or [configured](#configuring) text editor. It can also print out or
return a string of this metadata instead.


Why?
----

Sometimes you just need to read the source.

The Python Interpreter, `dir`, and `help` are fantastic tools for tinkering and
sanity checking. However, at times the only way to gain a better understanding
is to see what's going on below the surface. Spending the time searching or
tracking down where an object is defined can be tedious and distracting.

Now all you have to remember is `hack(<object>)`.

#### Use cases

- Read the source of a function when its documentation is unclear or incomplete
- Quickly jump to a package you're developing when tinkering in the interpreter
- Explore a dependency to confirm a bug without having to learn its file layout


Installation
------------

```bash
$ pip install hack-function
```

After installing, the `hack` function will be available globally.


Usage
-----

View the source of an object in your code editor:

```py
>>> import os
>>> hack(os.path.isabs)
```

You can also view it directly in the interpreter:

```py
>>> hack(os.path.isabs, 'source')
def isabs(s):
    """Test whether a path is absolute"""
    s = os.fspath(s)
    s = splitdrive(s)[1]
    return len(s) > 0 and s[0] in _get_bothseps(s)
```

Or print just the path and line number:

```py
>>> hack(os.path.join, 'path')
/usr/lib/python3.5/posixpath.py:62
```

Each action can also be aliased by its first character:

```py
>>> hack(os.path, 'p')
/usr/lib/python3.5/posixpath.py
```

And some actions can be configured further:

```py
>>> out = hack(os.path.isabs, 's', capture=True)
>>> out.split('\n')[0]
'def isabs(s):\n'
```

Take a look at the `hack` source code for more details:

```py
>>> hack(hack)
```


Configuring
-----------

By default, `hack` takes a best-guess of which text editor to use. You can
override this by setting one of the following to your editor's run command:
- The contents of `~/.hack-function`
- The `EDITOR` environment variable
- The `HACK_FUNCTION_EDITOR` environment variable

In the above, `$FILE` will be replaced with the filename to open and `$LINE`
with the line number. If these aren't preset, the filename will be appended
to the command.

#### Examples

Linux and Mac:

```bash
$ EDITOR="vi +\$LINE \$FILE" python
>>> hack(hack)
```

Windows:

```batch
>SET EDITOR="C:\Program Files\Sublime Text 3\sublime_text.exe" $FILE:$LINE
>py
>>> hack(hack)
```

Or persist one of the above `EDITOR` values in a `~/.hack-function` file.

Additional notes
----------------

- `hack` will not work on builtin objects and modules (since they're likely implemented outside of Python code)
- `hack` uses the `inspect` module internally (look here if you need programmatic access to this information)


Contributing
------------

1. Check the open issues or open a new issue to start a discussion around
   your feature idea or the bug you found
2. Fork the repository and make your changes
3. Open a new pull request

If your PR has been waiting a while, feel free to [ping me on Twitter](https://twitter.com/joeyespo).
