from abc import ABC, abstractmethod


class Frame(ABC):

    @abstractmethod
    def __repr__(self) -> str:
        pass


class LinearFrame(Frame):

    def __init__(self):
        self._string = ""
        self._level = 0
        self._level_spaces = {}

    def __repr__(self) -> str:
        return self._string[:-1]

    def _get_space(self, level: int) -> int:
        return self._level_spaces.get(level, 3) * self._level

    def add_line(self, line: str) -> None:
        self._string += " " * self._get_space(self._level)
        self._string += line
        self._string += "\n"

    def add_empty_line(self) -> None:
        self._string += "\n"

    def set_level(self, level: int) -> None:
        self._level = level

    def set_indention(self, level: int, indention: int) -> None:
        self._level_spaces[level] = indention


class Formatter:
    pass


f = LinearFrame()
f.add_line("Hallo")
f.set_level(1)
f.add_line("Welt")
f.set_level(0)
f.add_line("Wie gehts")
print(f)
