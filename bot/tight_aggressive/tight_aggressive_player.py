# -*- coding: utf-8 -*-


from .. import base_player
import tight_aggressive_bot

class tight_aggressivePlayer(base_player.BasePlayer):
  def __init__(self):
  	super(tight_aggressivePlayer, self).__init__()
  	self.current_bot = tight_aggressive_bot.TightAggressiveBot(self)
  
  def new_game(self, parts):
    super(tight_aggressivePlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(tight_aggressivePlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(tight_aggressivePlayer, self).handover(parts)
