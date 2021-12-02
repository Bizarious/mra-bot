from abc import ABC, abstractmethod
from typing import Callable


class APILayer(ABC):
    """
    The template class for the api calling interface.
    """

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def add_message_handler(self, cmd: Callable) -> None:
        pass
