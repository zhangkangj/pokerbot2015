from .. import base_player
import base_nash_bot

import mixedoppnew_bot

import mixedoppnew_opponent

import fold_bot


class Base_nashPlayer(base_player.BasePlayer):
  def __init__(self):
    super(Base_nashPlayer, self).__init__()
    self.current_bot = mixedoppnew_bot.MixedoppnewBot(self) ## by defalt it uses mixed_opp_new
    self.nash_bot1 = base_nash_bot.Base_nashBot(self, 30, ' ')
    self.current_bot_type = 'MIXED'


  def new_game(self, parts):
    super(Base_nashPlayer, self).new_game(parts)
    
    
  def new_hand(self, parts):
    super(Base_nashPlayer, self).new_hand(parts);
    if self.num_active_player == 2 and (self.current_bot_type != 'NASH'):
    	self.current_bot = self.nash_bot1
    	#self.current_bot = base_nash_bot.Base_nashBot(self, 100, ' ')
    	self.current_bot_type = 'NASH'
    	print 'Now change to nash bot for new hand'
    elif self.num_active_player == 3 and (self.current_bot_type != 'MIXED'):
    	self.current_bot = mixedoppnew_bot.MixedoppnewBot(self)
    	self.current_bot_type = 'MIXED'
    	print 'Now change to mixed bot for new hand'
    else:
    	print 'Current player:' + self.current_bot_type
    
  def handover(self, parts):
    super(Base_nashPlayer, self).handover(parts)


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


  def action(self,parts):
  	super(Base_nashPlayer, self).action(parts);
  	if self.num_active_player_dynamic == 2 and (self.current_bot_type != 'NASH'):
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
#		self.current_bot = base_nash_bot.Base_nashBot(self, 100, ' ')
		self.current_bot_type = 'NASH'
    	###############!!!!!!!!!!!!!!!!!!!!!!!!!##################
    	#### INIT bot based on last_actions_init lists!!########
    	##
    	##
    	##
    	##
		




## here are copied from mixedoppnew_player.py
  def create_opponents(self):
    self.opp1 = mixedoppnew_opponent.MixedoppnewOpponent(self.opp1_name, self);
    self.opp2 = mixedoppnew_opponent.MixedoppnewOpponent(self.opp2_name, self);

  def discount_equity_for_opponent(self, original_equity, max_discount_factor=0):
    opponent_equity_discount = self.eval_opponents() * max_discount_factor
    discounted_equity = (1-opponent_equity_discount) * original_equity
    return discounted_equity  

  def eval_opponents(self):
    max_opp_eval_result = 1
    min_opp_eval_result = 0
    less_opp_eval_threshold = 0.7
    less_opp_eval_factor = 0.5

    # default value to no effect by the opponents
    result = min_opp_eval_result

    eval_opp_results=[]

    for opponent in self.opponents:
      if opponent.is_active_in_game and opponent.is_active_in_hand: 
       # call opponent's evaulation  
        eval_result = opponent.eval_opponent()    
        eval_opp_results.append(eval_result)
    
    if len(eval_opp_results) > 1:
      # if we evaluated two opponents
      max_opp_eval = max(eval_opp_results)
      min_opp_eval = min(eval_opp_results)

      # if the other opponent is also a significant threat 
      if min_opp_eval > less_opp_eval_threshold * max_opp_eval_result:
        result = max_opp_eval + (max_opp_eval_result - max_opp_eval) * less_opp_eval_factor

    elif len(eval_opp_results) == 1:
      result = eval_opp_results[0]
    
    return result 