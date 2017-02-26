# -*- coding: cp1252 -*-
"""This module implementes IRC bot class"""
import sys
import socket
import libirc
from handlers import *

_BUFFERSIZE = 4096

# Pakolliset tiedot
class Bot(libirc.Irc):
    """IRC Bot class"""

    def __init__(self, nickname, username, real_name):
        """Initializes the Bot

        Set ups bot's nickname and socket

        Args:
            nickname (string): Name wanted to show on the channel
        """
        self._nickname = nickname
        self._username = username
        self._real_name = real_name
        self._channel = None
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def quit(self):
        """Sends IRC QUIT command
        """
        self.send("QUIT")
        self.stop()

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

            # At this point we know we are not dealing with IRC command, but channel message instead
            try:
                channel_msg = " ".join(incoming_msg.split()[3:])
                # Check if we got '!cmd'
                if channel_msg[1] == '!':
                    print "bang detected"
                    self._handle_bangs(channel_msg[2:])
            except IndexError:
                pass

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
