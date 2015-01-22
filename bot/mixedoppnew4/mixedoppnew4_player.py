from .. import base_player
import mixedoppnew4_bot

import mixedoppnew4_opponent

class Mixedoppnew4Player(base_player.BasePlayer):
  def __init__(self):
    super(Mixedoppnew4Player, self).__init__()
    self.current_bot = mixedoppnew4_bot.Mixedoppnew4Bot(self)
  
  def new_game(self, parts):
    super(Mixedoppnew4Player, self).new_game(parts)
    
  def new_hand(self, parts):
    super(Mixedoppnew4Player, self).new_hand(parts)
    
  def handover(self, parts):
    super(Mixedoppnew4Player, self).handover(parts)

  def create_opponents(self):
    #debug
    print "-------------###--Mixedoppnew4Player.create_opponents()"
    self.opp1 = mixedoppnew4_opponent.Mixedoppnew4Opponent(self.opp1_name, self);
    self.opp2 = mixedoppnew4_opponent.Mixedoppnew4Opponent(self.opp2_name, self);

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
    max_opp_eval_result = 1
    min_opp_eval_result = 0
    less_opp_eval_threshold = 0.7
    less_opp_eval_factor = 0.5

    # default value to no effect by the opponents
    result = min_opp_eval_result

    #debug
    print "----------====> enter eval_opponents() "
    #debug
    print "----------====> active_players: " + str(self.active_players)
    eval_opp_results=[]

    for opponent in self.opponents:
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
      if min_opp_eval > less_opp_eval_threshold * max_opp_eval_result:
        result = max_opp_eval + (max_opp_eval_result - max_opp_eval) * less_opp_eval_factor

      #debug  
      print "------------====> opp eval result with max, min: " + str(result)
    elif len(eval_opp_results) == 1:
      result = eval_opp_results[0]
    else:
      print "------------====> ERORR: no eval result generated"
    
    #debug
    print "----------====> exit eval_opponents(), eval result: " + str(result)
    
    return result 
