from .. import base_player
import mixednew_bot

class MixednewPlayer(base_player.BasePlayer):
  def __init__(self):
    super(MixednewPlayer, self).__init__()
    self.current_bot = mixednew_bot.MixednewBot(self)
  
  def new_game(self, parts):
    super(MixednewPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(MixednewPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(MixednewPlayer, self).handover(parts)
