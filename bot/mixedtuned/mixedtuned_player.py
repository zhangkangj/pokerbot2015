from .. import base_player
import mixedtuned_bot

class MixedtunedPlayer(base_player.BasePlayer):
  def __init__(self):
    super(MixedtunedPlayer, self).__init__()
    self.current_bot = mixedtuned_bot.MixedtunedBot(self)
  
  def new_game(self, parts):
    super(MixedtunedPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(MixedtunedPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(MixedtunedPlayer, self).handover(parts)
