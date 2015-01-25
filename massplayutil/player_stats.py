class PlayerStats(object):
  def __init__(self, player):
    self.player = player
    self.win = 0
    self.second = 0
    self.third = 0
    self.total_game_end_stack = 0