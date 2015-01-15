from .. import base_player
import playbig_1_bot

class Playbig_1Player(base_player.BasePlayer):
  def __init__(self):
    self.current_bot = playbig_1_bot.Playbig_1Bot(self)
  
  def new_game(self, parts):
    super(Playbig_1Player, self).new_game(parts)
    
  def new_hand(self, parts):
    super(Playbig_1Player, self).new_hand(parts)
    
  def handover(self, parts):
    super(Playbig_1Player, self).handover(parts)
