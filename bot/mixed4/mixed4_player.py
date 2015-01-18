from .. import base_player
import mixed4_bot

class Mixed4Player(base_player.BasePlayer):
  def __init__(self):
    super(Mixed4Player, self).__init__()
    self.current_bot = mixed4_bot.Mixed4Bot(self)
    self.current_stacksize = None
  
  def new_game(self, parts):
    super(Mixed4Player, self).new_game(parts)
    
  def new_hand(self, parts):
    super(Mixed4Player, self).new_hand(parts)
    
  def handover(self, parts):
    super(Mixed4Player, self).handover(parts)

  def action(self, parts):
    super(Mixed4Player, self).action(parts)
    print '-----------stack_sizes:' + str(self.stack_sizes) + ', seat:' + str(self.seat)
    self.current_stacksize = int(self.stack_sizes[int(self.seat-1)])
    print '-----------self.current_stacksize:' + str(self.current_stacksize)
