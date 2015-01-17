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
    self.max_num_hand = None
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
    self.num_active_player = None
    self.active_players = None
    self.timebank = None
    self.num_board_card = None
    self.board_cards = None
    self.pot_size = None
    self.num_last_action = None
    self.last_actions = None
    self.num_legal_action = None
    self.legal_actions = None
    self.action_state=None

  def new_game(self, parts):
    self.player_name = parts[1]
    self.opp1_name = parts[2]
    self.opp2_name = parts[3]
    self.game_init_stack_size = int(parts[4])
    self.bb_size = int(parts[5])
    self.max_num_hand = int(parts[6])
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
    self.num_active_player = self.init_num_active_player
    self.active_players = self.init_active_players
    self.init_timebank = float(parts[15])
    self.timebank = self.init_timebank
    self.board_cards = []
    self.num_board_card = 0
    self.last_actions_preflop = []
    self.last_actions_flop=[]
    self.last_actions_turn=[]
    self.last_actions_river=[]
    self.action_state='PREFLOP';

  def action(self, parts):
    self.pot_size = int(parts[1])
    self.num_board_card = int(parts[2])
    self.board_cards = parts[3:(3+self.num_board_card)]
    index = 3+self.num_board_card
    self.stack_sizes = [int(x) for x in parts[index:(index+3)]]
    index = index + 3
    self.num_active_player = int(parts[index])
    index = index + 1
    self.active_players = [True if x == 'true' else False for x in parts[index:(index+3)]]
    index = index + 3
    self.num_last_action = int(parts[index])
    index = index + 1
    self.last_actions = parts[index:(index+self.num_last_action)]
    
    for last_action in self.last_actions:
      tempstr = last_action.split(':')
      if len(tempstr) == 2 and ('DEAL' not in last_action): # check or fold, not Deal
        lastelm = None;
      elif len(tempstr) == 3:
        lastelm = int(tempstr[1]);
      elif 'DEAL' in last_action:
        self.action_state = tempstr[-1]
        continue
      else:
        print "Error: Last Action parsing wrong"
      if self.action_state == 'PREFLOP': 
        self.last_actions_preflop.append((tempstr[-1],tempstr[0],lastelm))
      elif self.action_state=='FLOP':
        self.last_actions_flop.append((tempstr[-1],tempstr[0],lastelm));
      elif self.action_state == 'TURN':
        self.last_actions_turn.append((tempstr[-1],tempstr[0],lastelm));
      elif self.action_state == 'RIVER':
        self.last_actions_river.append((tempstr[-1],tempstr[0],lastelm));
      else:
        print "Error: action_state wrong"
    print 'self.last_actions_preflop:', self.last_actions_preflop;
    print 'self.last_actions_flop:', self.last_actions_flop;
    print 'self.last_actions_turn:', self.last_actions_turn;
    print 'self.last_actions_river:', self.last_actions_river;
    index = index + self.num_last_action
    self.num_legal_action = int(parts[index])
    index = index + 1
    self.legal_actions = parts[index:(index+self.num_legal_action)]
    index = index + self.num_legal_action
    self.timebank = float(parts[index])




  def handover(self, parts):
    self.stack_sizes = [int(x) for x in parts[1:4]]
    self.num_board_card = int(parts[4])
    self.board_cards = parts[5:(5+self.num_board_card)]
    index = 5 + self.num_board_card
    self.num_last_action = int(parts[index])
    index = index + 1
    self.last_actions = parts[index:(index+self.num_last_action)]
    index = index + self.num_last_action
    self.timebank = float(parts[index])
    print

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
      self.action(parts)
      result = self.current_bot.action()
    elif word == 'HANDOVER':
      self.handover(parts)
      self.current_bot.handover()
    elif word == 'REQUESTKEYVALUES':
      # this is called by the end of a match
      result = self.set_key_value() + '\n'
      result += self.current_bot.set_key_value() + '\n'
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
        traceback.print_exc()
        print data
        result = None
      if result is not None:
        print result
        input_socket.send(result + '\n')
    input_socket.close()
