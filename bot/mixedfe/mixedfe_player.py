from .. import base_player
import mixedfe_bot

class MixedfePlayer(base_player.BasePlayer):
  def __init__(self):
    super(MixedfePlayer, self).__init__()
    self.current_bot = mixedfe_bot.MixedfeBot(self)
  
  def new_game(self, parts):
    super(MixedfePlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(MixedfePlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(MixedfePlayer, self).handover(parts)
