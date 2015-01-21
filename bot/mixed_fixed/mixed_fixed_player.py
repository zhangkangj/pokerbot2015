from .. import base_player
import mixed_fixed_bot

class Mixed_fixedPlayer(base_player.BasePlayer):
  def __init__(self):
    super(Mixed_fixedPlayer, self).__init__()
    self.current_bot = mixed_fixed_bot.Mixed_fixedBot(self)
  
  def new_game(self, parts):
    super(Mixed_fixedPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(Mixed_fixedPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(Mixed_fixedPlayer, self).handover(parts)
