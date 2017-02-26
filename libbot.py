# -*- coding: cp1252 -*-
"""This module implementes IRC bot class"""
import sys
import socket
from handlers import *

_BUFFERSIZE = 4096

# Pakolliset tiedot
class Bot(object):
    """IRC Bot class"""

    def __init__(self, nickname):
        """Initializes the Bot

        Set ups bot's nickname and socket

        Args:
            nickname (string): Name wanted to show on the channel
        """
        self._nickname = nickname
        self._channel = None
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, cmd):
        """Use initialized socket to send cmd
        Adds carriage return by default
        """
        print '{}\r\n'.format(cmd)
        self._socket.send('{}\r\n'.format(cmd))

    def chat(self, msg, channel=None):
        """Send normal chat message to given channel

        Args:
            msg (string): message you wish to send
            channel (string): name of the channel, self._channel by default
        """
        if channel in [None, 'None', '']:
            channel = self._channel
        self.send('PRIVMSG {} :{}'.format(channel, msg))

    def connect_to_network(self, network, port=6667):
        """Open connection to IRC network

        Opens socket to given network and port. Sets nickname and user information.

        Args:
            network (string): address of the network (e.g. "irc.quakenet.org")
            port (int): port number to connect to (default IRC port is 6667)
        """
        self._socket.connect((network, port))
        not_checked_ident = True
        while not_checked_ident:
            msg = self._socket.recv(_BUFFERSIZE)
            if msg not in [None, 'None', '']:
                print msg
            if msg[:4] == 'PING':
                self._handle_ping_pong(msg)
            if 'Ident' in msg:
                not_checked_ident = False
        set_userinfo_cmd = 'USER kujis botti bottimies :koijaari'
        set_nickname_cmd = 'NICK {}'.format(self._nickname)
        self.send(set_nickname_cmd)
        self.send(set_userinfo_cmd)
        # Wait until MOTD is received, now we know we are connected for sure
        motd_not_received = True
        while motd_not_received:
            msg = self._socket.recv(_BUFFERSIZE)
            if msg[:4] == 'PING':
                self._handle_ping_pong(msg)
            if 'MOTD' in msg:
                motd_not_received = False

    def join_channel(self, channel):
        """Joins a IRC channel

        Args:
            channel (string): name of the channel you with the bot to join
        """
        mark = '#'
        if '@' in channel:
            mark = '@'
        channel = channel.replace('#', '').replace('@', '')
        channel = '{}{}'.format(mark, channel)
        self.send('JOIN {}'.format(channel))
        self.chat('Heippa maailma.', channel)
        self._channel = channel

    def quit(self):
        """Sends IRC QUIT command
        """
        self.send("QUIT")
        self.stop()

    def _auto_rejoin(self):
        """If kicked, rejoin the channel
        """
        self.join_channel(self._channel)

    def _handle_ping_pong(self, cmd):
        """Handle PONG response to PING

        Args:
            cmd (string): full PING message
        """
        timestamp = cmd.split()[1]
        self.send('PONG {}'.format(timestamp))

    def _handle_bangs(self, cmd):
        """Handle !cmd commands

        Args:
            cmd (string): command without '!' mark
        """
        bang = cmd.split()[0]
        print 'cmd:', cmd
        print 'bang:', bang
        msg = None

        if bang in ['quit', 'die', 'part', 'lopeta', 'kuole']:
            self.chat('Mie meen pois')
            self.quit()

        if bang in ['moi', 'terve', 'hei', 'hi', 'hello']:
            msg = say_hello()

        if bang in ['k', 'q', 'kysymys', 'question', 'oracle', 'ennuste', 'enustus', 'prediction']:
            msg = get_prediction(cmd[1:])

        if bang in ['horo', 'horoskooppi', 'horoscope']:
            msg = get_horoscope(cmd.split()[1])

        if bang in ['nimpparit', 'nimipäivät', 'nimipäivä', 'nimppari']:
            msg = get_nameday()

        if bang in ['sl', 'sananlasku', 'sananlaskut', 'sanonta', 'sanonnat', 'proverb']:
            msg = get_proverb()

        if msg is not None:
            self.chat(msg)

    def stop(self):
        """kills the bot
        """
        sys.exit(0)

    def start(self):
        """Start listening for incoming messages and handle them
        """
        while True:
            incoming_msg = self._socket.recv(_BUFFERSIZE)
            if incoming_msg not in [None, 'None', '']:
                print incoming_msg

            if incoming_msg[:4] == 'PING':
                self._handle_ping_pong(incoming_msg)

            if incoming_msg[:4] == 'KICK':
                self._auto_rejoin()

            # OK, at this point we are not dealing with IRC command, but channel message
            try:
                channel_msg = " ".join(incoming_msg.split()[3:])

                # Check if we got '!cmd'
                if channel_msg[1] == '!':
                    print "bang detected"
                    self._handle_bangs(channel_msg[2:])

            except IndexError:
                pass
