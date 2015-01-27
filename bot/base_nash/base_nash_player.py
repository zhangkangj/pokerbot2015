from .. import base_player
from bot.mixedoppnew6 import mixedoppnew6_bot
from bot.mixedoppnew6 import mixedoppnew6_opponent
#from bot.tight_aggressive import tight_aggressive_bot
#from bot.tight_conservative import tight_conservative_bot
from bot.mixed import mixed_bot

import base_nash_bot

class Base_nashPlayer(base_player.BasePlayer):
  def __init__(self):
    super(Base_nashPlayer, self).__init__()
    self.opponew6 = mixedoppnew6_bot.Mixedoppnew6Bot(self)
    self.mixed_bot = mixed_bot.MixedBot(self)
     ## by defalt it uses mixedoppnew6
    self.nash_bot_300 = base_nash_bot.Base_nashBot(self, 300, '../../data/cfr/aws_new/prob_300_total.npy')
 #   self.nash_bot_300 = []
    self.nash_bot_200 = []
    self.nash_bot_140 = []
    self.nash_bot_90 = []
    self.nash_bot_50 = []
    self.nash_bot_25 = []
    self.nash_bot_10 = []
#    self.nash_bot_200 = base_nash_bot.Base_nashBot(self, 200, '../../data/cfr/aws/prob_300_total.npy')
#    self.nash_bot_140 = base_nash_bot.Base_nashBot(self, 140, '../../data/cfr/aws/prob_300_total.npy')
#    self.nash_bot_90 = base_nash_bot.Base_nashBot(self, 90, '../../data/cfr/aws/prob_300_total.npy')
#    self.nash_bot_50 = base_nash_bot.Base_nashBot(self, 50, '../../data/cfr/aws_new/prob4_50_total.npy')
#    self.nash_bot_25 = base_nash_bot.Base_nashBot(self, 25, '../../data/cfr/aws_new/prob4_25_total.npy')
#    self.nash_bot_10 = base_nash_bot.Base_nashBot(self, 10, '../../data/cfr/aws/prob_300_total.npy')
#    self.tight_aggressive_bot1 = tight_aggressive_bot.TightAggressiveBot(self)
#    self.tight_conservative_bot1 = tight_conservative_bot.TightConservativeBot(self)
    self.current_bot = self.opponew6
    self.current_bot_type = 'MIXED'
    self.Bankrolls={};



  def new_game(self, parts):
    print 
    print '****New Game Start*******'
    super(Base_nashPlayer, self).new_game(parts)
    if len(self.Bankrolls) == 0:
      print 'This is the first game:INIT bankrolls'
      self.Bankrolls[self.player_name]=0
      self.Bankrolls[self.opp1_name] = 0
      self.Bankrolls[self.opp2_name] = 0    
    
    #print 'call create_op,......................'
    #self.create_opponents();

  def new_hand(self, parts):
    super(Base_nashPlayer, self).new_hand(parts);
    if self.num_active_player == 2 and (self.current_bot_type != 'NASH'):
      if self.init_stack_sizes[self.seat-1] > 200:
        self.current_bot = self.nash_bot_300;
      elif self.init_stack_sizes[self.seat-1] > 140:
        self.current_bot = self.nash_bot_200;
      elif self.init_stack_sizes[self.seat-1] > 90:
        self.current_bot = self.nash_bot_140;
      elif self.init_stack_sizes[self.seat-1] > 50:
        self.current_bot = self.nash_bot_90;
      elif self.init_stack_sizes[self.seat-1] > 25:
        self.current_bot = self.nash_bot_50;
      elif self.init_stack_sizes[self.seat-1] > 10:
        self.current_bot = self.nash_bot_25;
      else:
        self.current_bot = self.nash_bot_10;
    	#self.current_bot = base_nash_bot.Base_nashBot(self, 100, ' ')
      #Max add the following line, for now, only use nash_300
      self.current_bot = self.nash_bot_300
      self.current_bot_type = 'NASH'
      print 'Now change to nash bot for new hand'
    elif self.num_active_player == 3: #and (self.current_bot_type == 'NASH'):
      if self.stack_rank == 3 and min(self.stack_sizes) < 50 and max(self.stack_sizes) > 450:
        self.current_bot = self.mixed
 #       self.current_bot = self.opponew6
        self.current_bot_type = 'TIGHT_CONSERVATIVE'
        print "Should use tight here - depend on whether second person is tight";
      elif self.stack_rank == 3 and min(self.stack_sizes) < 50 and max(self.stack_sizes) < 350:
        self.current_bot = self.mixed
  #      self.current_bot = self.opponew6
        self.current_bot_type = 'TIGHT_AGGRESSIVE'
        print "Should use tight aggressive here"
      elif self.stack_rank == 2 and self.stack_sizes[self.seat-1] < 100:
        self.current_bot = self.mixed
    #    self.current_bot = self.opponew6
        print "Should use tight conservative here"
        self.current_bot_type = 'TIGHT_CONSERVATIVE'
      else:
        print "Should use normal here"
        self.current_bot = self.opponew6
        self.current_bot_type = 'MIXED'
        print 'Now change to mixedoppnew6 bot for new hand'
    else:
    	print 'Current player:' + self.current_bot_type
    
  def handover(self, parts):
    super(Base_nashPlayer, self).handover(parts)
    if max(self.stack_sizes) == 600: # the last hand in a game
       # the last one already omitted. SO it is the last one in player_names
      self.Bankrolls[self.player_names[-1]] += -80;
      if self.stack_sizes[0] == 0:
        self.Bankrolls[self.player_names[0]] += -20
        self.Bankrolls[self.player_names[1]] += 100;
      else:
        self.Bankrolls[self.player_names[0]] += 100
        self.Bankrolls[self.player_names[1]] += -20;
      print '****************Current BANKROLLS:'+ str(self.Bankrolls)


  def prepare_last_actions(self,active_name,inactive_name,last_acts):
    modified_acts = [];
    modstate=0
    for act in last_acts:
      if (act[0] != inactive_name) and (modstate == 0):
        modified_acts.append(act);
      elif (act[0] == active_name) and (modstate == 1):
        modstate = 0;
        newtup = (act[0],'RAISE',act[-1])
        modified_acts.append(newtup)
      elif (act[0] == self.player_name) and (modstate == 1):
        modstate = 0;
        newtup = (act[0],'RAISE',act[-1]);
        modified_acts.append(newtup)
      elif act[0] == inactive_name:
        if ('RAISE' not in act[1]) and ('BET' not in act[1]):
          pass
        else:
          if len(modified_acts) == 0:
            modstate = 1;
          else:
            lastelm = modified_acts.pop()
            if lastelm[0] == active_name:
              newtup = (lastelm[0],'RAISE',act[-1])
              modified_acts.append(newtup)
            else:
              modstate = 1
              modified_acts.append(lastelm)
      else:
        print 'ERROR in mapping 3->2 in base_nash_player'
    return modified_acts

  def further_process_init(self,last_actions_xxx_init):
    # cannot end with two calls
    if len(last_actions_xxx_init) > 2 and last_actions_xxx_init[-1][1] == 'CALL' and last_actions_xxx_init[-2][1] == 'CALL':
      last_actions_xxx_init.pop()
    # call/check cannot before raise/bet
    if len(last_actions_xxx_init) > 2:
      raiseflag = 0;
      for i in range(-1,-len(last_actions_xxx_init)-1,-1):
        if last_actions_xxx_init[i][1] in ['RAISE','BET']:
          raiseflag = 1;
        elif raiseflag == 1 and last_actions_xxx_init[i][1] in ['CALL','CHECK']:
          newtup = (last_actions_xxx_init[i][0],'RAISE',max(0,last_actions_xxx_init[i][2])+1);
          last_actions_xxx_init[i] = newtup;
          raiseflag = 0;
    return last_actions_xxx_init

  def action(self,parts):
    super(Base_nashPlayer, self).action(parts);
    if self.num_active_player_dynamic == 2 and self.action_state != 'PREFLOP' and (self.current_bot_type != 'NASH'):
      print 'Now change to nash bot for new action'
      print 'self.last_actions_preflop:'+str(self.last_actions_preflop);
      print 'self.last_actions_flop:', self.last_actions_flop;  
      print 'self.last_actions_turn:', self.last_actions_turn;
      print 'self.last_actions_river:', self.last_actions_river;
      self.last_actions_preflop_init = self.prepare_last_actions(self.active_name,self.inactive_name,self.last_actions_preflop)
      self.last_actions_flop_init = self.prepare_last_actions(self.active_name,self.inactive_name,self.last_actions_flop)
      self.last_actions_turn_init = self.prepare_last_actions(self.active_name,self.inactive_name,self.last_actions_turn)
      self.last_actions_river_init = self.prepare_last_actions(self.active_name,self.inactive_name,self.last_actions_river)
      print 'last_actions_preflop_init:::' + str(self.last_actions_preflop_init)
      print 'last_actions_flop_init:::' + str(self.last_actions_flop_init)
      print 'last_actions_turn_init:::' + str(self.last_actions_turn_init)
      print 'last_actions_river_init:::' + str(self.last_actions_river_init)

      # if I am SB: I post 1, oppo1 posts2, oppo2 called/fold.
      if self.last_actions_preflop[0][0] == self.player_name and self.last_actions_preflop[2][1] in ['CALL','FOLD']:
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [(self.player_name,'POST',1),(self.active_name,'POST',2)]+self.last_actions_preflop_init
        # if used to conclude by check and now conclude by me: should conclude by him
        if self.last_actions_preflop_init[-1][0] == self.player_name and self.last_actions_preflop[-1][1] == 'CHECK':
          self.last_actions_preflop_init = self.last_actions_preflop_init + [(self.active_name,'CHECK',None)]
      # if I am SB: I post 1, oppo1 posts 2, oppo2 raised. then suppose I called and oppo raised
      elif self.last_actions_preflop[0][0] == self.player_name and self.last_actions_preflop_init[1][1] == 'RAISE':
        firstelm = self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [firstelm , (self.active_name,'POST',2) , (self.player_name,'CALL',2)] + self.last_actions_preflop_init
        # if I am BB and SB fold. I change to SB.I post1, oppo post 2, i called. then whatever.
      elif self.last_actions_preflop[1][0] == self.player_name and self.last_actions_preflop_init[0][0] == self.player_name and self.last_actions_preflop_init[0][1] == 'CALL':
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [(self.player_name,'POST',1),(self.active_name,'POST',2),(self.player_name,'CALL',2)] + self.last_actions_preflop_init
        # if last one is check. was conclued by me. should concluded by him.
        if self.last_actions_preflop[-1][1] == 'CHECK':
          self.last_actions_preflop_init.pop()
          self.last_actions_preflop_init.pop()
          self.last_actions_preflop_init = self.last_actions_preflop_init + [(self.active_name,'CHECK',None)]
       # if I am BB and SB fold, and I raised. I change to SB. i post 1, BB post 2, I raise
      elif self.last_actions_preflop[1][0] == self.player_name and self.last_actions_preflop_init[0][0] == self.player_name and self.last_actions_preflop_init[0][1] == 'RAISE': 
        self.last_actions_preflop_init.pop()
        self.last_actions_preflop_init.pop()
        self.last_actions_preflop_init = [(self.player_name,'POST',1),(self.active_name,'POST',2)] + self.last_actions_preflop_init
        # if I am BB and dealer fold. nothing changed.
      elif self.last_actions_preflop[1][0] == self.player_name and self.last_actions_preflop_init[1][0] == self.player_name:
        pass
      # if I am dealer and i called. then I am BB and start from SB.
      elif self.last_actions_preflop[2][0] == self.player_name and self.last_actions_preflop[2][1] == 'CALL':
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [(self.active_name,'POST',1) , (self.player_name,'POST',2)]+self.last_actions_preflop_init
        # I have to conclude the round. if last one is check. then oppo call and I check.
        if self.last_actions_preflop[-1][1] == 'CHECK':
          self.last_actions_preflop_init.pop()
          self.last_actions_preflop_init = self.last_actions_preflop_init + [(self.active_name,'CALL',2),(self.player_name,'CHECK',None)]
          # if I am dealer and I raised. Then I am BB and SB called, and I raised
      elif self.last_actions_preflop[2][0] == self.player_name and self.last_actions_preflop[2][1] == 'RAISE':            
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [(self.active_name,'POST',1) , (self.player_name,'POST',2) , (self.active_name,'CALL',2)]+self.last_actions_preflop_init
      else:
        print "Should be legal..."
        # delete redundant calls

      self.last_actions_preflop_init = self.further_process_init(self.last_actions_preflop_init)
      self.last_actions_flop_init = self.further_process_init(self.last_actions_flop_init)
      self.last_actions_turn_init = self.further_process_init(self.last_actions_turn_init)
      self.last_actions_river_init = self.further_process_init(self.last_actions_river_init)

      action_seq = self.last_actions_preflop_init      
      if self.num_board_card >= 3:
        action_seq = action_seq + [('FLOP', 'DEAL', None)] + self.last_actions_flop_init
      if self.num_board_card >= 4:
        action_seq = action_seq + [('TURN', 'DEAL', None)] + self.last_actions_turn_init
      if self.num_board_card >= 5:
        action_seq = action_seq + [('RIVER', 'DEAL', None)] + self.last_actions_river_init       

      print 'last_actions_preflop_init:::' + str(self.last_actions_preflop_init)
      print 'last_actions_flop_init:::' + str(self.last_actions_flop_init)
      print 'last_actions_turn_init:::' + str(self.last_actions_turn_init)
      print 'last_actions_river_init:::' + str(self.last_actions_river_init)

      # if max(len(self.last_actions_preflop_init),len(self.last_actions_flop_init),len(self.last_actions_turn_init),len(self.last_actions_river_init)) < 7:
      #   # max < 7 then can change bot
      
#grafting
#      if self.nash_bot1.initialize_from_beginning(action_seq):
#        self.current_bot = self.nash_bot1
#        self.current_bot_type = 'NASH'
      

    	###############!!!!!!!!!!!!!!!!!!!!!!!!!##################
    	#### INIT bot based on last_actions_init lists!!########
    	##
    	##
    	##
    	##

  def create_opponents(self):
    #debug
    print "-------------###--Mixedoppnew6Player.create_opponents()"
  
    # create a 'opponent model' 'opp0' for the player itself to store info for convenience
    self.opp0 = mixedoppnew6_opponent.Mixedoppnew6Opponent(self.player_name, self);
    # create models for the actual opponents
    self.opp1 = mixedoppnew6_opponent.Mixedoppnew6Opponent(self.opp1_name, self);
    self.opp2 = mixedoppnew6_opponent.Mixedoppnew6Opponent(self.opp2_name, self);

    self.opponents = [self.opp0, self.opp1, self.opp2];    
    print self.opp1

  def discount_equity_for_opponent(self, original_equity, max_discount_factor=0):
    #debug
    print "-------------discount_equity_for_opponent(), original_equity: " + str(original_equity) + ", active_players: " + str(self.active_players)
    opponent_equity_discount = self.eval_opponents() * max_discount_factor
    #debug
    print "-------------discount_equity_for_opponent(), opponent_equity_discount: " + str(opponent_equity_discount) + ", original equity:" + str(original_equity)
    discounted_equity = (1-opponent_equity_discount) * original_equity
    #debug
    print "-------------discount_equity_for_opponent(), oppo discounted equity:" + str(discounted_equity)
    return discounted_equity  

  def eval_opponents(self):
    max_opp_eval_limit = 1
    min_opp_eval_limit = 0
    less_opp_eval_threshold = 0.7

    # default value to no effect by the opponents
    result = min_opp_eval_limit

    #debug
    print "----------====> enter eval_opponents() "
    #debug
    print "----------====> active_players: " + str(self.active_players)
    eval_opp_results=[]

    # get actual opponents - 1st element is the player itself
    opponents = self.opponents[1:]
    

    for opponent in opponents:
      if opponent.is_active_in_game and opponent.is_active_in_hand: 
        #debug
        print "--------------====> about to evaluate opponent: " + str(opponent.oppo_name)
        # call opponent's evaulation  
        eval_result = opponent.eval_opponent()    
        eval_opp_results.append(eval_result)
        print "--------------====> completed evaluating opponent, eval_result:" + str(eval_result) + ", for: " + str(opponent.oppo_name) 
    
    print "------------====> completed evaluating all opponents, eval_opp_results:" + str(eval_opp_results)
    
    if len(eval_opp_results) > 1:
      # if we evaluated two opponents
      max_opp_eval = max(eval_opp_results)
      min_opp_eval = min(eval_opp_results)
      #debug
      print "------------====> max_opp_eval: " + str(max_opp_eval) + ", min_opp_eval: " + str(min_opp_eval) 

      # if the other opponent is also a significant threat 
      if min_opp_eval > less_opp_eval_threshold * max_opp_eval_limit:
        result = max_opp_eval + (max_opp_eval_limit - max_opp_eval) * min_opp_eval

      #debug  
      print "------------====> opp eval result with max, min: " + str(result)
    elif len(eval_opp_results) == 1:
      result = eval_opp_results[0]
    else:
      print "------------====> ERORR: no eval result generated"
    
    #debug
    print "----------====> exit eval_opponents(), eval result: " + str(result)
    
    return result 
		
