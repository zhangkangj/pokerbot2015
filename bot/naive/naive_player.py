from .. import base_player
import naive_bot

class NaivePlayer(base_player.BasePlayer):
  def __init__(self):
    super(LayeredPlayer, self).__init__()
    self.current_bot = naive_bot.NaiveBot(self)
  
  def new_game(self, parts):
    super(NaivePlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(NaivePlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(NaivePlayer, self).handover(parts)
