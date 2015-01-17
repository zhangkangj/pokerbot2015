from .. import base_player
import fold_bot

class FoldPlayer(base_player.BasePlayer):
  def __init__(self):
  	super(FoldPlayer, self).__init__()
  	self.current_bot = fold_bot.FoldBot(self)
  
  def new_game(self, parts):
    super(FoldPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(FoldPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(FoldPlayer, self).handover(parts)
