class BaseUJMLError(Exception):
    '''Base class for all ujml related exceptions.'''
    def __init__(self, filename, lineno):
        super().__init__()
        self.__filename = filename
        self.__lineno = lineno

    def _error_message(self):
        return 'This message should never be shown. If you are reading this then someone is either raising a ' \
               'BaseUJMLError or forgot to override the _error_message() function.'

    def __str__(self):
        return '\n    File "{}", line {}\n        '.format(self.__filename, self.__lineno)+self._error_message()


class RootMustBeUJMLError(BaseUJMLError):
    '''Raised when the root element is not a ujml element.'''
    def __init__(self, filename, lineno):
        super().__init__(filename, lineno)

    def _error_message(self):
        return "The root element must a 'ujml' element."


class ReadOnlyAttributeError(BaseUJMLError):
    '''Raised when attempting to modify a readonly ujml attribute.'''
    def __init__(self, filename, lineno, attr_name):
        super().__init__(filename, lineno)
        self.attr_name = attr_name

    def _error_message(self):
        return "Attempting to modify readonly attribute '{}'.".format(self.attr_name)


class UnknownProcessingInstructionError(BaseUJMLError):
    '''Raised when an unrecognized processing instruction is read.'''
    def __init__(self, filename, lineno, pi_name):
        super().__init__(filename, lineno)
        self.pi_name = pi_name

    def _error_message(self):
        return "Unknown processing instructiion '{}'.".format(self.pi_name)


class UnknownElementError(BaseUJMLError):
    '''Raised when an unknown element is read.'''
    def __init__(self, filename, lineno, elem_name):
        super().__init__(filename, lineno)
        self.elem_name = elem_name

    def _error_message(self):
        return "Unknown element '{}'.".format(self.elem_name)


class IncompatibleUJVersion(BaseUJMLError):
    '''Raised when the required Urban Journey version is incompatible with the one installed.'''
    def __init__(self, filename, lineno, ver_required, ver_installed):
        super().__init__(filename, lineno)
        self.ver_required = ver_required
        self.ver_installed = ver_installed

    def _error_message(self):
        return "Urban Journey version '{}' was found but '{}' is required.".format(self.ver_installed, self.ver_required)


class InvalidAttributeInputError(BaseUJMLError):
    def __init__(self, filename, lineno, elem_name, attrib_name):
        super().__init__(filename, lineno)
        self.elem_name = elem_name
        self.atrib_name = attrib_name

    def _error_message(self):
        return 'Attribute {} at element {} has invalid input. This may be a type or syntax error.'\
            .format(self.atrib_name, self.elem_name)


class InvalidElementInputError(BaseUJMLError):
    def __init__(self, filename, lineno, elem_name):
        super().__init__(filename, lineno)
        self.elem_name = elem_name

    def _error_message(self):
        return 'Element {} has invalid input. This may be a type, value or syntax error.'\
            .format(self.elem_name)


class IdMustBeUniqueError(BaseUJMLError):
    def __init__(self, filename, lineno, id):
        super().__init__(filename, lineno)
        self.id = id

    def _error_message(self):
        return "Id '{}' already exists."\
            .format(self.id)


class InvalidChildError(BaseUJMLError):
    '''Raised when an element is not a valid child of the parent element.'''
    def __init__(self, filename, lineno, parent_name, child_name):
        super().__init__(filename, lineno)
        self.parent_name = parent_name
        self.child_name = child_name

    def _error_message(self):
        return "Element '{}' is not a valid child of '{}'".format(self.child_name, self.parent_name)


class UJMLError(BaseUJMLError):
    '''Generic UJML exception that only takes a message as parameter.'''
    # This exception exists only because I'm sometimes to lazy to create a new exception class.
    def __init__(self, filename, lineno, msg):
        super().__init__(filename, lineno)
        self.msg = msg

    def _error_message(self):
        return self.msg


class DataLoadError(BaseUJMLError):
    """Error while loading data."""
    def __init__(self, filename, lineno, data_element_name):
        super().__init__(filename, lineno)
        self.data_element_name = data_element_name

    def _error_message(self):
        return "Error loading data at data element '{}'.".format(self.data_element_name)


class RequiredAttributeError(BaseUJMLError):
    """An ujml element is missing a required attribute."""
    def __init__(self, filename, lineno, element_name, attribute_name):
        super().__init__(filename, lineno)
        self.element_name = element_name
        self.attribute_name = attribute_name

    def _error_message(self):
        return "Element '{}' is missing required attribute '{}'.".format(self.element_name, self.attribute_name)


class IdNotFoundError(BaseUJMLError):
    """No element was found with the target id."""
    def __init__(self, filename, lineno, id):
        super().__init__(filename, lineno)
        self.id = id

    def _error_message(self):
        return "No element was found with id '{}'.".format(self.id)


class InvalidDataElement(BaseUJMLError):
    """This error is raised when an non data element has been passed where a data element was expected"""
    def __init__(self, filename, lineno, element_name):
        super().__init__(filename, lineno)
        self.element_name = element_name

    def _error_message(self):
        return "'{}' is not  valid data element.".format(self.element_name)


class UJMLTypeError(BaseUJMLError, TypeError):
    """This error is raised whenever a parameter of invalid type has been passed."""
    def __init__(self, filename, lineno, element_name):
        super().__init__(filename, lineno)
        self.element_name = element_name

    def _error_message(self):
        return "Element '{}' received data of invalid type".format(self.element_name)


class InvalidShapeError(BaseUJMLError):
    """This error is raised whenever a parameter of invalid shape has been passed."""
    def __init__(self, filename, lineno, element_name):
        super().__init__(filename, lineno)
        self.element_name = element_name

    def _error_message(self):
        return "Element '{}' received data of invalid shape".format(self.element_name)


class InvalidInputError(BaseUJMLError):
    """Raised when invalid input was given."""
    def __init__(self, filename, lineno, element_name):
        super().__init__(filename, lineno)
        self.element_name = element_name

    def _error_message(self):
        return "Invalid input at '{}'.".format(self.element_name)


class MissingRequiredInput(BaseUJMLError):
    """This error is raised whenever a required input was not given to a module."""
    def __init__(self, filename, lineno, module_name, input_name):
        super().__init__(filename, lineno)
        self.module_name = module_name
        self.input_name = input_name

    def _error_message(self):
        return "Module '{}' is missing required input '{}'.".format(self.module_name, self.input_name)
