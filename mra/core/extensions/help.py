from core.ext import ExtensionHandler
from core.commands import command, BotExtension, bot_extension


@bot_extension()
class Help(BotExtension):

    @command()
    def help(self, ctx):
        handler: ExtensionHandler = self.interface.extension_handler
        extensions = handler.extensions
