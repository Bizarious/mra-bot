class ExtensionPackage:

    def __init__(self, cls: type):
        self.__cls = cls

    @property
    def cls(self):
        return self.__cls


def extension():
    def decorator(cls: type):
        return ExtensionPackage(cls)
    return decorator


class Extension:
    """
    This class is used to extend functionality in different ways.
    """

    def __init__(self):
        pass

    @property
    def name(self):
        return self.__class__.__name__
