# -*- coding: cp1252 -*-
"""This module implementes IRC bot class"""
import socket
import urllib2

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

    def chat(self, msg, channel=self._channel):
        """Send normal chat message to given channel

        Args:
            msg (string): message you wish to send
            channel (string): name of the channel, self._channel by default
        """
        self.send('PRIVMSG #{} :{}'.format(channel, msg))

    def connect_network(self, network, port=6667):
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
        self._channel = channel
        self.send('JOIN #{}'.format(self._channel))
        self.chat('Heippa maailma.', channel)

    def quit(self):
        """Sends IRC QUIT command
        """
        self.send("QUIT")

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

    def _oracle(self, question):
        """Asks a question from oracle and echoes it to channel

        Args:
            question (string): question to be asked from the oracle
        """
        # Sanitize question for URL
        clean_question = urllib2.quote(question)
        orcale_url = 'http://www.lintukoto.net/viihde/oraakkeli/index.php?kysymys={}&html'\
                .format(clean_question)
        oracle_request = urllib2.Request(orcale_url)
        oracle_response = urllib2.urlopen(oracle_request)
        answer = oracle_response.read()
        self.chat(answer)

    def _daily_horoscope(self, horoscope):
        """Asks a daily horoscope and echoes it to channel

        Args:
            horoscope (string):
        """

        print horoscope

        horoscopes = ['oinas','härkä','kaksonen','rapu','leijona','neitsyt','vaaka','skorpioni','jousimies','kauris','vesimies','kalat']
        horoscope = horoscope.lower()
        if horoscope in horoscopes:
            horoscope_url = 'http://www.iltalehti.fi/horoskooppi/'
            horoscope_request = urllib2.Request(horoscope_url)
            horoscope_response = urllib2.urlopen(horoscope_request)
            content = horoscope_response.read()
            find = '<p>{}'.format(horoscope)
            splitdata = content.split(find, 1)
            answer = splitdata[1].split('</p>', 1)
            self.chat(horoscope + answer[0])
        else:
            self.chat('En ymmärtänyt')

    def _handle_bangs(self, cmd):
        """Handle !cmd commands

        Args:
            cmd (string): command without '!' mark
        """
        bang = cmd.split()[0]
        print cmd
        print bang

        if bang in ['quit', 'die', 'part', 'lopeta', 'kuole']:
            self.chat('Mie meen pois')
            self.quit()

        if bang in ['moi', 'terve', 'hei', 'hi', 'hello']:
            self.chat('Moro')

        if bang == 'k':
            self._oracle(cmd[1:])

        if bang in ['horo', 'horoskooppi', 'horoscope']:
            self._daily_horoscope(cmd[5:])

    def stop(self):
        """FIXME: TODO"""
        pass

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

#TODO: These should be in separate file which imports Bot class
KUJIS = Bot('kujis_testi3')
KUJIS.connect_network('irc.quakenet.org')
KUJIS.join_channel('kujalla')
KUJIS.start()
