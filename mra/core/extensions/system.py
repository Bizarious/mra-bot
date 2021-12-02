from core.ext import Extension, extension
from core.commands import command


@extension()
class System(Extension):

    @command()
    def test(self):
        print("Hello World")


