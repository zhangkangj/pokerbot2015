from .. import base_player
import mixed1_bot

class Mixed1Player(base_player.BasePlayer):
  def __init__(self):
    super(Mixed1Player, self).__init__()
    self.current_bot = mixed1_bot.Mixed1Bot(self)
    self.current_stacksize = None
  
  def new_game(self, parts):
    super(Mixed1Player, self).new_game(parts)
    
  def new_hand(self, parts):
    super(Mixed1Player, self).new_hand(parts)
    
  def handover(self, parts):
    super(Mixed1Player, self).handover(parts)

  def action(self, parts):
    super(Mixed1Player, self).action(parts)
    print '-----------stack_sizes:' + str(self.stack_sizes) + ', seat:' + str(self.seat)
    self.current_stacksize = int(self.stack_sizes[int(self.seat-1)])
    print '-----------self.current_stacksize:' + str(self.current_stacksize)
