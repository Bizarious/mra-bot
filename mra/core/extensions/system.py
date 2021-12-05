from core.ext import extension
from core.commands import command, BotExtension, group


@extension()
class System(BotExtension):

    @command()
    def hello(self, ctx):
        ctx.reply("Hello")

    @command()
    def stop(self, _):
        self.interface.stop_bot()

    @command()
    def restart(self, _):
        self.interface.restart_bot()

    @group()
    def test(self, ctx, a):
        ctx.send(a)

    @test.command()
    def test2(self, ctx, a):
        ctx.send(int(a)+1)

