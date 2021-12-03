from core.ext import Extension, extension
from core.commands import command


@extension()
class System(Extension):

    @command()
    def test(self, ctx):
        ctx.send("Test")

    @command()
    def hello(self, ctx):
        ctx.reply("Hello")

    @command()
    def stop(self, _):
        self.interface.stop_bot()


