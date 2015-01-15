# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 13:13:18 2015

@author: zhk
"""

import argparse
import socket
import sys

from bot.playbig_layered import playbig_layered_player

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
  parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
  parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
  args = parser.parse_args()

  # Create a socket connection to the engine.
  print 'Connecting to %s:%d' % (args.host, args.port)
  try:
    s = socket.create_connection((args.host, args.port))
  except socket.error as e:
    print 'Error connecting! Aborting'
    exit()

  bot = playbig_layered_player.Playbig_layeredPlayer()
  bot.run(s)
