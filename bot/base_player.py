import base_opponent

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
    self.opponents = None

    self.current_stacksize = None

  def new_game(self, parts):
    self.player_name = parts[1]
    self.opp1_name = parts[2]
    self.opp2_name = parts[3]
    self.game_init_stack_size = int(parts[4])
    self.bb_size = int(parts[5])
    self.max_num_hand = int(parts[6])
    self.game_init_timebank = float(parts[7])

    self.create_opponents();
    self.opponents = [self.opp1, self.opp2];

  def create_opponents(self):
    #debug
    print "-------------###--MixedoppnewPlayer.create_opponents()"    
    self.opp1 = base_opponent.BaseOpponent(self.opp1_name, self);
    self.opp2 = base_opponent.BaseOpponent(self.opp2_name, self);

  def key_value(self, parts):
    pass

  def new_hand(self, parts):

    print "-------====>enter: new_hand()"

    # self.opp1 = base_opponent.BaseOpponent(self.opp1_name);
    # self.opp2 = base_opponent.BaseOpponent(self.opp2_name);
    # self.opponents = [self.opp1,self.opp2];

    for opponent in self.opponents:
      # clear the stats in opponents
      opponent.reset()

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

    self.player_names = parts[8:11]

    # since the sequence changes every hand, we need to grap the data by finding the index
    # for each player
    opp1_idx = -1
    opp2_idx = -1
    player_idx = -1

    for i in range(0,2):
      if self.player_names[i] == self.opp1.oppo_name:
        opp1_idx = i 
      elif self.player_names[i] == self.opp2.oppo_name:
        opp2_idx = i
      elif self.player_names[i] == self.player_name:
        player_idx = i
      else: 
        print "-------======>ERROR: self.player_names[" + str(i) + "]=" + str(self.player_names[i]) + " is not a valid name for player or opponents"
    
    self.opp1.is_active_in_game = bool(self.active_players[opp1_idx]) 
    self.opp1.stack_size_new_hand = int(self.stack_sizes[opp1_idx])

    self.opp2.is_active_in_game = bool(self.active_players[opp2_idx]) 
    self.opp2.stack_size_new_hand = int(self.stack_sizes[opp2_idx])   

    print "-------======>self.opp1.oppo_name: " + str(self.opp1.oppo_name) + ", self.opp1.is_active_in_game:" + str(self.opp1.is_active_in_game) + ", self.opp1.stack_size_new_hand:" + str(self.opp1.stack_size_new_hand)
    print "-------======>self.opp2.oppo_name: " + str(self.opp2.oppo_name) + ", self.opp2.is_active_in_game:" + str(self.opp1.is_active_in_game) + ", self.opp2.stack_size_new_hand:" + str(self.opp1.stack_size_new_hand)

    print "-------====>exit: new_hand()..."

  def UpdateOpponents(self,action_state,one_action):

    #debug
    print "-------======> enter UpdateOpponents(): action_state: " + str(action_state) + ", one_action: " + str(one_action)
       
    if self.opp1.is_active_in_game and self.opp1.is_active_in_hand and (self.opp1_name in one_action[-1]):
      print "-------========> action is for oppo1: " + self.opp1.oppo_name + ", one_action:" + str(one_action)
      self.opp1.Oppo_update(action_state,one_action[:-1]);
    elif self.opp2.is_active_in_game and self.opp2.is_active_in_hand and (self.opp2_name in one_action[-1]):
      print "-------========> action is for oppo2: " + self.opp2.oppo_name + ", one_action:" + str(one_action)
      self.opp2.Oppo_update(action_state,one_action[:-1]);
    elif self.player_name in one_action[-1]:
      print "-------========> action is for player, not opponent, one_action:" + str(one_action)
    else:
      print "-------========> ERROR: it is not possible to have both opponent (in-hand or in-game) inactive or if they are active, there is no action message for their last actions"

  def action(self, parts):
    #debug
    print "-------======> enter action(), parts:" + str(parts)
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
    
    
    
    last_actions_tmp = []
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
      
      # Update Opponents with last action str
      last_actions_tmp.append((tempstr[-1],tempstr[0],lastelm))
      self.UpdateOpponents(self.action_state,tempstr)

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
    self.last_actions = last_actions_tmp
    index = index + self.num_last_action
    self.num_legal_action = int(parts[index])
    index = index + 1
    self.legal_actions = parts[index:(index+self.num_legal_action)]
    index = index + self.num_legal_action
    self.timebank = float(parts[index])

    print '-----------stack_sizes:' + str(self.stack_sizes) + ', seat:' + str(self.seat)
    self.current_stacksize = int(self.stack_sizes[int(self.seat-1)])
    print '-----------self.current_stacksize:' + str(self.current_stacksize)


  def handover(self, parts):

    # print 'handover: self.last_actions_preflop:', self.last_actions_preflop;
    # print 'handover: self.last_actions_flop:', self.last_actions_flop;
    # print 'handover: self.last_actions_turn:', self.last_actions_turn;
    # print 'handover: self.last_actions_river:', self.last_actions_river;

    # print self.opponents[1].oppo_name
    # for action in self.opponents[1].all_actions:
    #   print 'handover: action.state:'+str(action.state) + "----------"
    #   print 'handover: action.call_seqs:'+str(action.call_seqs)
    #   print 'handover: action.call_amounts'+str(action.call_amounts)
    #   print 'handover: action.raise_seqs'+str(action.raise_seqs)
    #   print 'handover: action.raise_amounts'+str(action.raise_amounts)
    #   print 'handover: action.bet_seqs'+str(action.bet_seqs)
    #   print 'handover: action.bet_amounts'+str(action.bet_amounts)
    #   print 'handover: action.post_seqs'+str(action.post_seqs)
    #   print 'handover: action.post_amounts'+str(action.post_amounts)
    #   print 'handover: action.check_seqs'+str(action.check_seqs)
    #   print 'handover: handover: action.fold_seqs'+str(action.fold_seqs)
    #   print 'handover: action.action_count'+str(action.action_count)


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

