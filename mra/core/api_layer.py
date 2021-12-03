from abc import ABC, abstractmethod
from typing import Callable
from core.commands import Context


class APILayer(ABC):
    """
    The template class for the api calling interface.
    """

    def __init__(self, *, prefix: str):
        self._prefix = prefix

    @property
    def prefix(self) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self, prefix) -> None:
        self._prefix = prefix

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def add_message_handler(self, cmd: Callable) -> None:
        pass

    @abstractmethod
    def create_context(self, *args, **kwargs) -> Context:
        pass

    @abstractmethod
    def send_message(self, chat_id: int, message: str) -> None:
        pass

    @abstractmethod
    def reply_to_message(self, chat_id: int, message: str, message_id: int) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def on_command_error(self, ctx: Context, exception: Exception) -> None:
        pass


class APICommandAdapter:
    """
    Adapter for easier communication between api and api layer
    """

    def __init__(self, api_layer: APILayer, command_handler):
        self._api_layer = api_layer
        self._command_handler = command_handler  # no type here because of circular imports

    def translate(self, *args, **kwargs) -> None:
        context = self._api_layer.create_context(*args, **kwargs)
        try:
            self._command_handler.handle_command(context, self._api_layer.prefix)
        except Exception as e:
            try:
                self._api_layer.on_command_error(context, e)
            except NotImplementedError:
                print(f"Ignoring Exception:\n{e}")
