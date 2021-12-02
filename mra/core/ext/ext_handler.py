from importlib.util import spec_from_file_location, module_from_spec
from abc import ABC, abstractmethod
from .extension import Extension, ExtensionPackage
import os


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


class ExtensionHandler(ABC):
    """
    The class used to manage extensions.
    """

    def __init__(self, *paths: str):
        self._loader = ExtensionLoader()
        self._paths = paths

        self._accessible_types = []
        self._extension_classes = {}

    def _add_extension_class(self, name: str, extension: Extension) -> None:
        if name in self._extension_classes:
            raise RuntimeError(f'The extension "{name}" already exists')
        self._extension_classes[name] = extension

    def _load_extension_file(self, name: str, path: str) -> None:
        # loading module
        spec = spec_from_file_location(name, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        extension_packages: [ExtensionPackage] = self._loader.get_attributes(module,
                                                                             ["ExtensionPackage"]
                                                                             )["ExtensionPackage"]
        for extension_package in extension_packages:
            self._add_extension_class(extension_package.name, extension_package.cls)

    def load_extensions_from_paths(self) -> None:
        """
        Loads all extension classes that are found in the paths to the list.
        """
        for path in self._paths:
            for file in os.listdir(path):
                if not file.startswith("__"):
                    self._load_extension_file(file[:-3], path+f"/{file}")


class ExtensionHandlerFeature:

    def __init__(self, types: list, t: str):
        types.append(t)


if __name__ == "__main__":
    e = ExtensionHandler("../../core/extensions")
    e.load_extensions_from_paths()
