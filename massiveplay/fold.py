# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 13:13:18 2015

@author: zhk
"""

import argparse
import socket
import sys

from bot.fold import fold_player

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

  import os
  print "------------dir-----------"
  print os.path.dirname(os.path.realpath("."))
  f = open('../../massive_params.txt', 'r')
  # f = open('../../massive_params.txt', 'r')
  lineStr = f.readline()
  print "lineStr: " + str(lineStr)
  line = lineStr.split(', ')
  print "line: " + str(line)
  param1 = line[0]
  param2 = line[1]
  f.close()

  print "-----------------------"
  print "line: " + str(line)
  print "param1: " + str(param1)
  print "param2: " + str(param2)
  print "param1+2: " + str(param1+param2)
  print "-----------------------"

  bot = fold_player.FoldPlayer()
  bot.run(s)
