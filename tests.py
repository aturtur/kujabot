# -*- coding: cp1252 -*-
# pylint: disable=no-member
"""Tests for irc library"""
import unittest
import mock
import libbot


class BotTests(unittest.TestCase):
    """Main test suite"""
    def setUp(self):
        self.bot = libbot.Bot('test_bot')

    def tearDown(self):
        with mock.patch('libbot.Bot.stop'):
            with mock.patch('libbot.Bot.send'):
                self.bot.quit()
                self.bot.send.assert_called_with('QUIT')

    def test_join_channel(self):
        """Test that join_channel() works as expected.

        Check that you can join both local (@) and global (#) channels.
        Check that channel name without prefix (@ or #) defaults to global (#) channel.
        Check that bot sends join message to correct channel after joining
        """
        with mock.patch('libbot.Bot.send'):
            join_msg = 'Heippa maailma.'
            self.bot.join_channel('#channel')
            self.bot.send.assert_called_with('PRIVMSG #channel :{}'.format(join_msg))
            self.bot.join_channel('@localchannel')
            self.bot.send.assert_called_with('PRIVMSG @localchannel :{}'.format(join_msg))
            self.bot.join_channel('default')
            self.bot.send.assert_called_with('PRIVMSG #default :{}'.format(join_msg))
            self.bot.join_channel('spädöm')
            self.bot.send.assert_called_with('PRIVMSG #spädöm :{}'.format(join_msg))

if __name__ == '__main__':
    unittest.main()
