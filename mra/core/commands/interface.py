from .ext_handler_mixin import CommandFeature
from core.ext import ExtensionInterface


class CommandInterface(ExtensionInterface):
    """
    An interface used to provide command extensions an controllable
    set of functionality.
    """
    def __init__(self, bot):
        ExtensionInterface.__init__(self, bot)

    @property
    def extension_handler(self) -> CommandFeature:
        return self._entity.extension_handler
