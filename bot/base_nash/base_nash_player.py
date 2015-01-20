from .. import base_player
#import base_nash_bot

import mixedoppnew_bot

import mixedoppnew_opponent

import fold_bot


class Base_nashPlayer(base_player.BasePlayer):
  def __init__(self):
	super(Base_nashPlayer, self).__init__()
	self.current_bot = mixedoppnew_bot.MixedoppnewBot(self) ## by defalt it uses mixed_opp_new
	self.current_bot_type = 'MIXED'


  def new_game(self, parts):
    super(Base_nashPlayer, self).new_game(parts)
    
    
  def new_hand(self, parts):
    super(Base_nashPlayer, self).new_hand(parts);
    if self.num_active_player == 2 and (self.current_bot_type != 'NASH'):
    	self.current_bot = fold_bot.FoldBot(self)
    	#self.current_bot = base_nash_bot.Base_nashBot(self, 100, ' ')
    	self.current_bot_type = 'NASH'
    	print 'Now change to nash bot for new hand'
    elif self.num_active_player == 3 and (self.current_bot_type != 'MIXED'):
    	self.current_bot = mixedoppnew_bot.MixedoppnewBot(self)
    	print 'Now change to mixed bot for new hand'
    else:
    	print 'Current player:' + self.current_bot_type
    
  def handover(self, parts):
    super(Base_nashPlayer, self).handover(parts)

  def action(self,parts):
  	super(Base_nashPlayer, self).action(parts);
  # 	if self.num_active_player_dynamic == 2 and (self.current_bot_type != 'NASH'):


  # 		# self.last_actions_preflop_init,self.last_actions_flop_init,self.last_actions_turn_init,self.last_actions_river_init = \
  # 		# self.prepare_last_actions(active_name,inactive_name,self.last_actions_preflop,self.last_actions_flop,self.last_actions_turn,self.last_actions_river);

		# self.current_bot = base_nash_bot.Base_nashBot(self, 100, ' ')
		# self.current_bot_type = 'NASH'
  #   	###############!!!!!!!!!!!!!!!!!!!!!!!!!##################
  #   	#### INIT bot based on last_actions_init lists!!########
  #   	##
  #   	##
  #   	##
  #   	##
  #   	print 'Now change to nash bot for new action'




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