from core.ext import extension
from core.commands import command, BotExtension


@extension()
class System(BotExtension):

    @command()
    def test(self, ctx):
        ctx.send("Test")

    @command()
    def hello(self, ctx):
        ctx.reply("Hello")

    @command()
    def stop(self, _):
        self.interface.stop_bot()

    @command()
    def restart(self, _):
        self.interface.restart_bot()
