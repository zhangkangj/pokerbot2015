# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 23:21:05 2015

@author: zhk
"""

from .. import base_player
import playbig_bot

class PlaybigPlayer(base_player.BasePlayer):
  def __init__(self):
  	super(PlaybigPlayer, self).__init__()
  	self.current_bot = playbig_bot.PlaybigBot(self)
  
  def new_game(self, parts):
    super(PlaybigPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(PlaybigPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(PlaybigPlayer, self).handover(parts)
