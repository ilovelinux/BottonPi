# -*- coding: utf-8 -*-
import logging.config
from irc3.plugins.command import command
import logging
import irc3


@irc3.plugin
class MyPlugin:
    """A plugin is a class which take the IrcBot as argument
    """

    requires = [
        'irc3.plugins.core',
        'irc3.plugins.userlist',
        'irc3.plugins.command',
#        'irc3.plugins.human',
    ]

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    def connection_made(self):
        """triggered when connection is up"""

    def server_ready(self):
        """triggered after the server sent the MOTD (require core plugin)"""

    def connection_lost(self):
        """triggered when connection is lost"""

#    @irc3.event(irc3.rfc.JOIN)
#    def welcome(self, mask, channel):
#        """Welcome people who join a channel"""
#        if mask.nick != self.bot.nick:
#            self.bot.call_with_human_delay(
#                self.bot.privmsg, channel, 'Benvenuto %s!' % mask.nick)
#        else:
#            self.bot.call_with_human_delay(
#                self.bot.privmsg, channel, "Ciao ragazzi!")

    @command
    def echo(self, mask, target, args):
        """Echo command

            %%echo <words>...
        """
        print(args)
        self.bot.privmsg(target, ' '.join(args['<words>']))

    @command
    def list(self, mask, target, args):
        """Show stats of the channel using the userlist plugin

            %%list
        """
        return 'Per la lista dare: /quit !list o /part !list.'

    @command
    def stats(self, mask, target, args):
        """Show stats of the channel using the userlist plugin

            %%stats [<channel>]
        """
        if args['<channel>']:
            channel = args['<channel>']
            target = mask.nick
        else:
            channel = target
        if channel in self.bot.channels:
            channel = self.bot.channels[channel]
            message = '{0} users'.format(len(channel))
            for mode, nicknames in sorted(channel.modes.items()):
                message += ' - {0}({1})'.format(mode, len(nicknames))
            self.bot.privmsg(target, message)

    @irc3.extend
    def my_usefull_method(self):
        """The extend decorator will allow you to call::

            bot.my_usefull_method()

        """


def main():
    # logging configuration
    logging.config.dictConfig(irc3.config.LOGGING)

    # instanciate a bot
    irc3.IrcBot(
        nick='TheButton', autojoins=['#python'],
        host='irc.azzurra.org', port=6669, ssl=False,
        includes=[
            'irc3.plugins.core',
            'irc3.plugins.command',
#            'irc3.plugins.human',
#            'modules.meteo',
#            'modules.utility',
#            'modules.news',
#            'modules.wiki',
#            'modules.search',
            __name__,  # this register MyPlugin
        ]).run()

if __name__ == '__main__':
    main()
