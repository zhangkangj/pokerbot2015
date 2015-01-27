# -*- coding: utf-8 -*-


from .. import base_player
import tight_conservative_bot

class tight_conservativePlayer(base_player.BasePlayer):
  def __init__(self):
  	super(tight_conservativePlayer, self).__init__()
  	self.current_bot = tight_conservative_bot.TightConservativeBot(self)
  
  def new_game(self, parts):
    super(tight_conservativePlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(tight_conservativePlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(tight_conservativePlayer, self).handover(parts)
