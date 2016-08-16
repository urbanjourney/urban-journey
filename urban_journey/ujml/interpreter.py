import sys


class UJMLPythonSourceClass(object):
    def __init__(self, source, filename, mode, lineno=0):
        self.__code = compile('\n'*(lineno-1)+source, filename, mode)
        self.__mode = mode
        self.__filename = filename
        self.__lineno = lineno

    @property
    def code(self):
        return self.__code

    @property
    def filename(self):
        return self.__filename

    @property
    def lineno(self):
        return self.__lineno


class UJMLPythonInterpreterClass(object):
    def __init__(self):
        self.globals = {}

    def __getitem__(self, key):
        return self.globals[key]

    def __setitem__(self, key, value):
        self.globals[key] = value

    def exec(self, source, filename, lineno):
        exec(compile('\n'*(lineno-1)+source, filename, 'exec'), self.globals)

    def run_src_object(self, src_obj):
        if isinstance(src_obj, UJMLPythonSourceClass):
            return eval(src_obj.code, self.globals)
        else:
            raise TypeError("Parameter should be of type 'UJMLPythonSourceClass'")

    def eval(self, source, filename, lineno):
        lines = source.strip().splitlines()
        locs = {}
        if len(lines) > 1:
            exec(compile('\n'*(lineno-1)+'\n'.join(lines[:-1]), filename, 'exec'), self.globals, locs)
        return eval(compile('\n'*(lineno-1+len(lines)-1)+lines[-1], filename, 'eval'), self.globals, locs)
