# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:27:09 2015

@author: zhk
"""

class BaseBot(object):
  
  def __init__(self, player):
    self.player = player
  
  def new_game(self):
    pass
  
  def new_hand(self):
    pass
  
  def action(self, *args, **kwargs):
    if self.player.num_board_card == 0:
      return self.preflop(*args, **kwargs)
    elif self.player.num_board_card == 3:
      return self.flop(*args, **kwargs)
    elif self.player.num_board_card == 4:
      return self.turn(*args, **kwargs)
    elif self.player.num_board_card == 5:
      return self.river(*args, **kwargs)
    else:
      raise Exception("invalid number board card")      
  
  def preflop(self, *args, **kwargs):
    raise NotImplementedError

  def flop(self, *args, **kwargs):
    raise NotImplementedError

  def turn(self, *args, **kwargs):
    raise NotImplementedError

  def river(self, *args, **kwargs):
    raise NotImplementedError

  def handover(self, *args, **kwargs):
    pass
  
  def set_key_value(self):
    return ''
