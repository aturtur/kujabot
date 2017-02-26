# -*- coding: cp1252 -*-
"""Main script to run kujabot"""
import libbot

def main():
    """Setup kujabot, connect to QuakeNet, and join #kujalla
    """
    kujis = libbot.Bot('kujabot')
    kujis.connect_to_network('irc.quakenet.org')
    kujis.join_channel('kujalla')
    kujis.start()

if __name__ == '__main__':
    main()
