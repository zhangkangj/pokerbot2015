import argparse
import socket
import sys

class BasePlayer(object):
  
  def __init__(self):
    self.current_bot = None
    self.opponent_model = None
    # game info
    self.player_name = None
    self.opp1_name = None
    self.opp2_name = None
    self.game_init_stack_size = None
    self.bb_size = None
    self.max_num_hands = None
    self.game_init_timebank = None
    # hand info
    self.hand_id = None # start with 0
    self.seat = None # 1-3
    self.hole_cards = None
    self.init_stack_sizes = None
    self.player_names = None # button, SB, BB
    self.init_num_active_player = None
    self.init_active_players = None
    self.init_timebank = None
    # round info
    self.stack_sizes = None
    self.num_active_players = None
    self.active_players = None
    self.timebank = None

  def new_game(self, parts):
    self.player_name = parts[1]
    self.opp1_name = parts[2]
    self.opp2_name = parts[3]
    self.game_init_stack_size = int(parts[4])
    self.bb_size = int(parts[5])
    self.max_num_hands = int(parts[6])
    self.game_init_timebank = float(parts[7])

  def key_value(self, parts):
    pass

  def new_hand(self, parts):
    self.hand_id = int(parts[1])
    self.seat = int(parts[2])
    self.hole_cards = parts[3:5]
    self.init_stack_sizes = [int(x) for x in parts[5:8]]
    self.stack_sizes = self.init_stack_sizes
    self.player_names = parts[8:11]
    self.init_num_active_player = int(parts[11])
    self.init_active_players = [True if x == 'true' else False for x in parts[12:15]]
    self.num_active_players = self.init_num_active_player
    self.active_players = self.init_active_players
    self.init_timebank = float(parts[16])
    self.timebank = self.init_timebank

  def handover(self, parts):
    pass

  def set_key_value(self):
    return ''

  def handle_message(self, message):
    result = None
    parts = message.split()
    word = parts[0]
    if word == 'NEWGAME':
      self.new_game(parts)
      self.current_bot.new_game()
    elif word == 'KEYVALUE':
      self.key_value(parts)
    elif word == 'NEWHAND':
      self.new_hand(parts)
      self.current_bot.new_hand()
    elif word == 'GETACTION':
      result = 'CHECK'
    elif word == 'HANDOVER':
      self.handover(parts)a
      self.current_bot.handover()
    elif word == 'REQUESTKEYVALUES':
      result = self.set_key_value()
      result += self.current_bot.set_key_value()
      result += 'FINISH'
    return result

  def run(self, input_socket):
    f_in = input_socket.makefile()
    while True:
      data = f_in.readline().strip()
      if not data:
        print 'Gameover, engine disconnected.'
        break
      print data
      try:
        result = self.handle_message(data)
      except:
        import traceback
        traceback.print_exec()
        print data
        result = None
      if result is not None:
        print result
        input_socket.send(result + '\n')
    input_socket.close()