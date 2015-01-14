# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 17:36:12 2015

@author: zhk
"""

from .. import util

def preflop(card1, card2):
  c1 = util.card_to_num(card1)
  c2 = util.card_to_num(card2)
  r1 = c1 / 4
  r2 = c2 / 4
  if r1 > r2:
    result = r1*(r1-1)/2 + r2
  elif r1 < r2:
    result = r2*(r2-1)/2 + r1
  else:
    result = 78 + r1
  if (c1&0b11) == (c2&0b11):
    result += 91
  return result