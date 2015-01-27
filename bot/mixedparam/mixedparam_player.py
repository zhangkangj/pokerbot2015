from .. import base_player
import mixedparam_bot

class MixedparamPlayer(base_player.BasePlayer):
  def __init__(self):
    super(MixedparamPlayer, self).__init__()
    self.current_bot = mixedparam_bot.MixedparamBot(self)
    self.param = None

  def set_param(self, param):
    self.param = param

  def new_game(self, parts):
    super(MixedparamPlayer, self).new_game(parts)
    
  def new_hand(self, parts):
    super(MixedparamPlayer, self).new_hand(parts)
    
  def handover(self, parts):
    super(MixedparamPlayer, self).handover(parts)
