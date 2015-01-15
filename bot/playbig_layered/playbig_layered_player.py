from .. import base_player
import playbig_layered_bot

class Playbig_layeredPlayer(base_player.BasePlayer):
  def __init__(self):
    super(LayeredPlayer, self).__init__()
    self.current_bot = playbig_layered_bot.Playbig_layeredBot(self)
  
  def new_game(self, parts):
    super(Playbig_layeredPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(Playbig_layeredPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(Playbig_layeredPlayer, self).handover(parts)
