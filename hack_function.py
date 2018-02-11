def hack(obj=None, action='open', capture=False, **kwargs):
    """
    Loads the object's source file at the line its defined on using the
    default or configured text editor.

    Run `hack(hack)` for details, or visit:
    https://github.com/joeyespo/hack-function
    """
    from os import environ, name as os_name
    from os.path import dirname, expanduser, join
    from sys import platform
    from subprocess import call
    from inspect import getmodule, getsource, getsourcefile, getsourcelines

    def read(filename):
        with open(join(dirname(__file__), filename)) as f:
            return f.read()

    def show(value):
        if capture:
            return value
        print(value)

    def edit(filename, lineno=None):
        editor = environ.get('HACK_FUNCTION_EDITOR', environ.get('EDITOR'))
        if editor is None:
            try:
                editor = read(expanduser(join('~', '.hack-function'))).strip()
            except EnvironmentError:
                pass
        if editor is not None:
            if '$FILE' in editor:
                editor = editor.replace('$FILE', filename)
            else:
                editor = ' '.join([editor, filename])
            if lineno:
                editor = editor.replace('$LINE', str(lineno))
            call(editor, shell=True)
            return editor
        elif platform.startswith('darwin'):
            call(('open', filename))
            return 'open {filename}'.format(filename=filename)
        elif os_name == 'posix':
            call(('xdg-open', filename))
            return 'xdg-open {filename}'.format(filename=filename)
        elif os_name == 'nt':
            from os import startfile

            try:
                startfile(filename, 'edit')
                return 'edit {filename}'.format(filename=filename)
            except EnvironmentError:
                startfile(filename)
                return 'start {filename}'.format(filename=filename)
        raise EnvironmentError('No editor found. Please set EDITOR variable.')

    def run():
        if action in ['o', 'open']:
            cmd = edit(getsourcefile(obj), getsourcelines(obj)[1])
            return show(cmd) if capture or kwargs.get('verbose') else None
        elif action in ['p', 'path']:
            components = [getsourcefile(obj)]
            if kwargs.get('line', True):
                lineno = getsourcelines(obj)[1]
                if lineno != 0:
                    components.append(str(lineno))
            return show(':'.join(components))
        elif action in ['p', 'path:only']:
            return show(getsourcefile(obj))
        elif action in ['m', 'module']:
            return show(getmodule(obj))
        elif action in ['s', 'source']:
            return show(read(getsourcefile(obj)) if kwargs.get('all') else
                        getsource(obj))
        raise ValueError('Unknown action {action}'.format(action=repr(action)))

    try:
        return run()
    except TypeError as ex:
        if capture:
            raise
        return show('Error: {message}'.format(message=ex))


def install():
    import sys

    builtins = sys.modules.get('builtins') or sys.modules.get('__builtin__')
    builtins.__dict__['hack'] = hack
