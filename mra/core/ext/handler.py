from importlib.util import spec_from_file_location, module_from_spec
from .extension import Extension, ExtensionPackage, ExtensionInterface
from .errors import ExtensionClassNotFoundError
import os


class ExtensionLoader:
    """
    The class used to load an extension from file.
    """

    @staticmethod
    def get_attributes(obj: object, *types: str) -> dict:
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

    def __init__(self, interface: ExtensionInterface, *paths: str):
        self._loader = ExtensionLoader()
        self._paths = paths
        self._interface = interface

        # collecting all types the handler can see
        self._accessible_types = []

        # list of functions that are executed on extension loading
        self._to_be_executed_on_extension_loading = []

        # maps all extension classes to their names
        self._extension_classes = {}

        # maps all loaded extension objects to their names
        self._extensions = {}

    def _add_extension_class(self, name: str, extension: Extension) -> None:
        if name in self._extension_classes:
            raise RuntimeError(f'The extension "{name}" already exists')
        self._extension_classes[name] = extension

    def _load_extension_from_file(self, name: str, path: str, *types: str) -> None:
        # loading module
        spec = spec_from_file_location(name, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        extension_packages: [ExtensionPackage] = self._loader.get_attributes(module,
                                                                             *types
                                                                             )["ExtensionPackage"]
        for extension_package in extension_packages:
            self._add_extension_class(extension_package.cls.__name__, extension_package.cls)

    def _load_extensions_from_paths_with_types(self, *package_types: str) -> None:
        """
        Loads all extension classes that are found in the paths to the list with given package types.
        Do not overwrite this function, overwrite load_extensions_from_path instead.
        """
        for path in self._paths:
            for file in os.listdir(path):
                if not file.startswith("__") and file.endswith(".py"):
                    self._load_extension_from_file(file[:-3], path + f"/{file}", *package_types)

    def load_extensions_from_paths(self):
        """
        Wrapper function for easier access. Can be overwritten.
        """
        self._load_extensions_from_paths_with_types("ExtensionPackage")

    def load_extension(self, name: str, *args, **kwargs) -> None:
        if name not in self._extension_classes:
            raise ExtensionClassNotFoundError(f'The extension class "{name}" does not exist')

        extension_class = self._extension_classes[name]
        extension = extension_class(self._interface, *args, **kwargs)
        attributes = self._loader.get_attributes(extension, *self._accessible_types)
        self._execute_on_loading(attributes, extension)
        self._extensions[name] = extension

    def _execute_on_loading(self, attributes: dict, extension: Extension) -> None:
        for func in self._to_be_executed_on_extension_loading:
            func(attributes, extension)


class ExtensionHandlerFeature:

    def __init__(self, types: list, t: str):
        types.append(t)
