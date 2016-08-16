class BaseDTSMLError(Exception):
    '''Base class for all dtsml related exceptions.'''
    def __init__(self, filename, lineno):
        super().__init__()
        self.__filename = filename
        self.__lineno = lineno

    def _error_message(self):
        return 'This message should never be shown. If you are reading this then someone is either raising a ' \
               'BaseDTSMLError or forgot to override the _error_message() function.'

    def __str__(self):
        return '\n    File "{}", line {}\n        '.format(self.__filename, self.__lineno)+self._error_message()


class ModifyingReadOnlyDTSMLAttributeError(Exception):
    '''Raised when a read-only attribute is being modified.'''
    def __str__(self):
        return "Read-only dtsml attribute is being modified"


class DTSMLTagMustBeRootError(BaseDTSMLError):
    '''Raised when a required attributed is missing.'''
    def __init__(self, filename, lineno):
        super().__init__(filename, lineno)

    def _error_message(self):
        return "Element 'dtsml' must be root element."


class UnknownProcessingInstructionError(BaseDTSMLError):
    '''Raised when a required attributed is missing.'''
    def __init__(self, filename, lineno, pi_name):
        super().__init__(filename, lineno)
        self.pi_name = pi_name

    def _error_message(self):
        return "Unknown processing instructiion '{}'.".format(self.pi_name)


class UnknownElementError(BaseDTSMLError):
    '''Raised when a required attributed is missing.'''
    def __init__(self, filename, lineno, elem_name):
        super().__init__(filename, lineno)
        self.elem_name = elem_name

    def _error_message(self):
        return "Unknown element '{}'.".format(self.elem_name)


class IncompatibleDTSTVersion(BaseDTSMLError):
    '''Raised when the required DTST version is incompatible with the one installed.'''
    def __init__(self, filename, lineno, ver_required, ver_installed):
        super().__init__(filename, lineno)
        self.ver_required = ver_required
        self.ver_installed = ver_installed

    def _error_message(self):
        return "DTST version '{}' was found but '{}' is required.".format(self.ver_installed, self.ver_required)


class InvalidAttributeInputError(BaseDTSMLError):
    def __init__(self, filename, lineno, elem_name, attrib_name):
        super().__init__(filename, lineno)
        self.elem_name = elem_name
        self.atrib_name = attrib_name

    def _error_message(self):
        return 'Attribute {} at element {} has invalid input. This may be a type or syntax error.'\
            .format(self.atrib_name, self.elem_name)


class InvalidElementInputError(BaseDTSMLError):
    def __init__(self, filename, lineno, elem_name):
        super().__init__(filename, lineno)
        self.elem_name = elem_name

    def _error_message(self):
        return 'Element {} has invalid input. This may be a type, value or syntax error.'\
            .format(self.elem_name)


class InvalidChildError(BaseDTSMLError):
    '''Raised when an element is not a valid child of the parent element.'''
    def __init__(self, filename, lineno, parent_name, child_name):
        super().__init__(filename, lineno)
        self.parent_name = parent_name
        self.child_name = child_name

    def _error_message(self):
        return "Element '{}' is not a valid child of '{}'".format(self.child_name, self.parent_name)


class DTSMLError(BaseDTSMLError):
    '''Generic DTSML exception that only takes a message as parameter.'''
    # This exception exists only because I'm sometimes to lazy to create a new exception class.
    def __init__(self, filename, lineno, msg):
        super().__init__(filename, lineno)
        self.msg = msg

    def _error_message(self):
        return self.msg


class DataLoadError(BaseDTSMLError):
    """Error while loading data."""
    # This exception exists only because I'm sometimes to lazy to create a new exception class.
    def __init__(self, filename, lineno, data_element_name):
        super().__init__(filename, lineno)
        self.data_element_name = data_element_name

    def _error_message(self):
        return "Error loading data at data element '{}'.".format(self.data_element_name)


class MissingRequiredAttributeError(BaseDTSMLError):
    """An dtsml element is missing a required attribute."""
    def __init__(self, filename, lineno, element_name, attribute_name):
        super().__init__(filename, lineno)
        self.element_name = element_name
        self.attribute_name = attribute_name

    def _error_message(self):
        return "Element '{}' is missing required attribute '{}'.".format(self.element_name, self.attribute_name)


class IdNotFoundError(BaseDTSMLError):
    """No element was found with the target id."""
    def __init__(self, filename, lineno, id):
        super().__init__(filename, lineno)
        self.id = id

    def _error_message(self):
        return "No element was found with id '{}'.".format(self.id)


class InvalidDataElement(BaseDTSMLError):
    """This error is raised when an non data element has been passed where a data element was expected"""
    def __init__(self, filename, lineno, element_name):
        super().__init__(filename, lineno)
        self.element_name = element_name

    def _error_message(self):
        return "'{}' is not  valid data element.".format(self.element_name)


class InvalidTypeError(BaseDTSMLError):
    """This error is raised whenever a parameter of invalid type has been passed."""
    def __init__(self, filename, lineno, element_name):
        super().__init__(filename, lineno)
        self.element_name = element_name

    def _error_message(self):
        return "Element '{}' received data of invalid type".format(self.element_name)


class InvalidShapeError(BaseDTSMLError):
    """This error is raised whenever a parameter of invalid shape has been passed."""
    def __init__(self, filename, lineno, element_name):
        super().__init__(filename, lineno)
        self.element_name = element_name

    def _error_message(self):
        return "Element '{}' received data of invalid shape".format(self.element_name)


class MissingRequiredInput(BaseDTSMLError):
    """This error is raised whenever a required input was not given to a module."""
    def __init__(self, filename, lineno, module_name, input_name):
        super().__init__(filename, lineno)
        self.module_name = module_name
        self.input_name = input_name

    def _error_message(self):
        return "Module '{}' is missing required input '{}'.".format(self.module_name, self.input_name)