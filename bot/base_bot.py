# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:27:09 2015

@author: zhk
"""

class BaseBot:
  
  def __init__(self, player):
    self.player = player
  
  def new_game(self):
    pass
  
  def new_hand(self):
    pass
  
  def preflop(self, *args, **kwargs):
    raise NotImplementedError

  def flop(self, *args, **kwargs):
    raise NotImplementedError

  def turn(self, *args, **kwargs):
    raise NotImplementedError

  def river(self, *args, **kwargs):
    raise NotImplementedError

  def handover(self, *args, **kwargs):
    raise NotImplementedError
  
  def set_key_value(self):
    return ''
