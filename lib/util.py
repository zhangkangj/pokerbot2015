# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 16:48:51 2015

@author: zhk
"""

import traceback

def num_to_card(n):
  if isinstance(n, basestring):
    return n
  else:
    rank = n / 4
    suit = n % 4
    if rank == 12:
        rank = "A"
    elif rank == 11:
        rank = "K"
    elif rank == 10:
        rank = "Q"
    elif rank == 9:
        rank = "J"
    elif rank == 8:
        rank = "T"
    else:
        rank = str(rank + 2)
    if suit == 0:
        suit = "s"
    elif suit == 1:
        suit = "h"
    elif suit == 2:
        suit = "d"
    elif suit == 3:
        suit = "c"
    else:
        raise Exception("suit error:" + str(n))
    return rank + suit

def card_to_num(card):
  if isinstance(card, basestring):
    rank = card[0]
    suit = card[1]
    if rank == "A":
        rank = 12
    elif rank == "K":
        rank = 11
    elif rank == "Q":
        rank = 10
    elif rank == "J":
        rank = 9
    elif rank == "T":
        rank = 8
    else:
        rank = int(rank) - 2
    if suit == "s":
        suit = 0
    elif suit == "h":
        suit = 1
    elif suit == "d":
        suit = 2
    elif suit == "c":
        suit = 3
    else:
        raise Exception("suit exception:" + suit)
    return suit + rank * 4
  else:
    return card

def n2c(numbers):
    return [number_to_card(x) for x in numbers]

def c2n(cards):
    return [card_to_number(x) for x in cards]

def tester(func):
  def inner(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except:
      trace.print_exc()
      print args, kwargs
      return None
  return inner

@tester
def test():
  print 'testing'
  import numpy as np
  print 'numpy version', np.__version__
  import platform
  print 'platform', platform.dist()
  import traceback
  try:
    from lib.evaluator import evaluator
  except:
    traceback.print_exc()
    print 'failed to import evaluator'
  try:
    from lib.evaluator import evaluator_cy
  except:
    traceback.print_exc()
    print 'failed to import evaluator_cy'
  try:
    from lib.card_abstraction import card_abs_cy
  except:
    traceback.print_exc()
    print 'failed to import lib.card_abs_cy'
  try:
    from study.card_abstraction import card_abs_cy
  except:
    traceback.print_exc()
    print 'failed to import study.card_abs_cy'
  print 'test done'
