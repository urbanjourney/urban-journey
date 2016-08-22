def tidy_source(code):
    """
    Strips and fixes the indentation of python code.
    eg.

    |    def foo():
    |        bar()

    or

    |def foo():
    |        bar()

    becomes

    |def foo():
    |    bar()
    """
    raw_lines = code.splitlines()
    lines = []

    # Remove all empty lines
    for line in raw_lines:
        if line.strip() != "":
            lines.append(line)

    if len(lines) > 1:
        if lines[0].rstrip()[-1] == ":":
            indents = 4  # If you don't use 4 spaces, you will break stuff.
        else:
            indents = 0
        lines[0] = lines[0].lstrip()
        remove = len(lines[1])-len(lines[1].lstrip())-indents
        code = lines[0]
        for idx in range(1, len(lines)):
                lines[idx] = lines[idx][remove:]
                code = "\n".join((code, lines[idx]))
    else:
        code = code.strip()
    return code


class UJMLPythonInterpreter:
    """Python embedded interpreter. All code executed here runs in it's own separate environment."""
    def __init__(self, globals=None):
        self.globals = globals or {}

    def __getitem__(self, key):
        """Dictionary like access to the interpreter globals"""
        return self.globals[key]

    def __setitem__(self, key, value):
        """Dictionary like access to the interpreter globals"""
        self.globals[key] = value

    def exec(self, source, file_name, source_line=1, is_global=False, **kwargs):
        """Executes python source code. Kwargs will be made available in the local scope."""
        source = tidy_source(source)
        # Locals
        locs = self.globals if is_global else kwargs
        exec(compile('\n' * (source_line - 1) + source, file_name, 'exec'),
             self.globals, locs)

    def eval(self, source, file_name, source_line=1, is_global=False, **kwargs):
        """Evaluates python source code. Kwargs will be made available in the local scope."""
        source = tidy_source(source)
        lines = source.strip().splitlines()
        locs = self.globals if is_global else kwargs
        if len(lines) > 1:
            exec(compile('\n' * (source_line - 1) + '\n'.join(lines[:-1]), file_name, 'exec'),
                 self.globals, locs)
        return eval(compile('\n' * (source_line - 1 + len(lines) - 1) + lines[-1], file_name, 'eval'),
                    self.globals, locs)


class UJMLPythonSource:
    """Compiles and stores a piece of python source code to be executed later."""
    def __init__(self, interpreter: UJMLPythonInterpreter, source, file_name, mode, source_line=1):
        source = tidy_source(source)
        # Perfect example of a buen oplossing right here. It's not possible to pass a line number to compile. So just
        # add a bunch of new lines at the beginning of the source code. This way exceptions tracebacks will show the
        # correct line number inside the ujml file.
        #                              |
        #                              V
        #                     |------------------|
        self.__code = compile('\n'*(source_line-1)+source, file_name, mode)
        self.__mode = mode
        self.__file_name = file_name
        self.__source_line = source_line
        self.__interpreter = interpreter

    @property
    def code(self):
        return self.__code

    @property
    def file_name(self):
        return self.__file_name

    @property
    def source_line(self):
        return self.__source_line

    def __call__(self, is_global=False, **kwargs):
        """Make this object callable."""
        locs = self.__interpreter.globals if is_global else kwargs
        return eval(self.__code, self.__interpreter.globals, locs)
