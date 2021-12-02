class ExtensionPackage:

    def __init__(self, cls: type, name: str):
        self.__cls = cls
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def cls(self):
        return self.__cls


def extension(alias: str = None):
    def decorator(cls: type):
        if alias is None:
            return ExtensionPackage(cls, cls.__name__)
        return ExtensionPackage(cls, alias)
    return decorator


class Extension:
    """
    This class is used to extend functionality in different ways.
    """

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name
