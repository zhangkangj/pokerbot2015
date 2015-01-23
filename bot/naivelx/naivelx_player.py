from .. import base_player
import naivelx_bot

class NaivelxPlayer(base_player.BasePlayer):
  def __init__(self):
  	super(NaivelxPlayer, self).__init__()
  	self.current_bot = naivelx_bot.NaivelxBot(self)
  
  def new_game(self, parts):
    super(NaivelxPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(NaivelxPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(NaivelxPlayer, self).handover(parts)
