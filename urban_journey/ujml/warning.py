
def print_ujml_warning(filename, lineno, warning_msg):
    print('WARNING: File "{}", line {}\n        '.format(filename, lineno)+warning_msg)


def unknown_element_warning(filename, lineno, element_name):
    print_ujml_warning(filename, lineno, 'Unknown element "{}".'.format(element_name))

