from .. import base_player
import mixedstronger_bot

class MixedstrongerPlayer(base_player.BasePlayer):
  def __init__(self):
    super(MixedstrongerPlayer, self).__init__()
    self.current_bot = mixedstronger_bot.MixedstrongerBot(self)
  
  def new_game(self, parts):
    super(MixedstrongerPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(MixedstrongerPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(MixedstrongerPlayer, self).handover(parts)
