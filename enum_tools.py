from enum import Enum


class NoValueEnum(Enum):
    """Enum to be subclassed when a specific value for each field is not needed.

    Set field values using auto(). See
    https://docs.python.org/3/library/enum.html?highlight=enum#omitting-values
    for more information.
    """

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self.name)
