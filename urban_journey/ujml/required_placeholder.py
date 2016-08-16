'''The Required variable in this module is used s a placeholder object in dtsml elements and attributes.'''


class RequiredType:
    def __repr__(self):
        return "Required"

    def __str__(self):
        return "Required"


class EmptyType:
    def __repr__(self):
        return "Empty"

    def __str__(self):
        return "Empty"

Required = RequiredType()
Empty = EmptyType()
