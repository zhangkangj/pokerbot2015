from .. import base_player
import base_nash_bot

class Base_nashPlayer(base_player.BasePlayer):
  def __init__(self):
  	super(Base_nashPlayer, self).__init__()
  	self.current_bot = base_nash_bot.Base_nashBot(self)
  
  def new_game(self, parts):
    super(Base_nashPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(Base_nashPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(Base_nashPlayer, self).handover(parts)
