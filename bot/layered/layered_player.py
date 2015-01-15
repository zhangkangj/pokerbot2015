from .. import base_player
import layered_bot

class LayeredPlayer(base_player.BasePlayer):
  def __init__(self):
    super(LayeredPlayer, self).__init__()
    self.current_bot = layered_bot.LayeredBot(self)
  
  def new_game(self, parts):
    super(LayeredPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(LayeredPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(LayeredPlayer, self).handover(parts)
