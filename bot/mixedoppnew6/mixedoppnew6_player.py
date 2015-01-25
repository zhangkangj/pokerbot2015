from .. import base_player
import mixedoppnew6_bot

import mixedoppnew6_opponent

class Mixedoppnew6Player(base_player.BasePlayer):
  def __init__(self):
    super(Mixedoppnew6Player, self).__init__()
    self.current_bot = mixedoppnew6_bot.Mixedoppnew6Bot(self)
  
  def new_game(self, parts):
    super(Mixedoppnew6Player, self).new_game(parts)
    
  def new_hand(self, parts):
    super(Mixedoppnew6Player, self).new_hand(parts)
    
  def handover(self, parts):
    super(Mixedoppnew6Player, self).handover(parts)

  def create_opponents(self):
    #debug
    print "-------------###--Mixedoppnew6Player.create_opponents()"
  
    # create a 'opponent model' 'opp0' for the player itself to store info for convenience
    self.opp0 = mixedoppnew6_opponent.Mixedoppnew6Opponent(self.player_name, self);
    # create models for the actual opponents
    self.opp1 = mixedoppnew6_opponent.Mixedoppnew6Opponent(self.opp1_name, self);
    self.opp2 = mixedoppnew6_opponent.Mixedoppnew6Opponent(self.opp2_name, self);

    self.opponents = [self.opp0, self.opp1, self.opp2];    

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
