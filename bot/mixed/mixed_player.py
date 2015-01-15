from .. import base_player
import mixed_bot

class MixedPlayer(base_player.BasePlayer):
  def __init__(self):
    self.current_bot = mixed_bot.MixedBot(self)
  
  def new_game(self, parts):
    super(MixedPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(MixedPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(MixedPlayer, self).handover(parts)
