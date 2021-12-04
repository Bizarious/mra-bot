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


class ExtensionInterface:
    """
    An interface used to provide extensions an controllable
    set of functionality.
    """
    pass


class Extension:
    """
    This class is used to extend functionality in different ways.
    """

    def __init__(self, interface: ExtensionInterface):
        self._interface = interface

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def interface(self):
        return self._interface


class ExtensionFeature:
    pass
