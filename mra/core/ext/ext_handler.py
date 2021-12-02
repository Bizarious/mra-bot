from importlib import import_module
from extension import ExtensionPackage


class ExtensionLoader:
    """
    The class used to load an extension from file.
    """

    @staticmethod
    def get_attributes(obj: object, types: [str]) -> dict:
        """
        Searches through an object and returns a dictionary that contains the given types
        mapped to all attributes of that object, that are instances of that type.
        """

        # preparing the dictionary
        attribute_mapping = {}
        for t in types:
            attribute_mapping[t] = []

        # searching through the object
        for attribute_name in dir(obj):
            attribute = getattr(obj, attribute_name)
            for t in types:
                if attribute.__class__.__name__ == t:
                    attribute_mapping[t].append(attribute)

        return attribute_mapping


class ExtensionHandler:
    """
    The class used to manage extensions.
    """

    def __init__(self, default_path: str):
        self._default_path = default_path
        self._loader = ExtensionLoader()

        self._accessible_types = []
        self._extension_classes = []

    def _load_extension_by_types(self, path: str, types: [str]) -> dict:
        module = import_module(path)
        return self._loader.get_attributes(module, types)

    def load_extension(self, path: str) -> None:
        pass


if __name__ == "__main__":
    e = ExtensionHandler("")
    e.load_extension("core.extensions.system")
