class ExtensionPackage:

    def __init__(self, cls):
        self.__cls = cls


def extension(cls):
    return ExtensionPackage(cls)


class Extension:
    """
    This class is used to extend functionality in different ways.
    """
    pass
