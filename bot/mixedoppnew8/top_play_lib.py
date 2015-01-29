import bot_action_lib

class TopPlayLib(object):

    # 0 - top_check_call
    # 1 - top_raise_max
    # 2 - top_raise_with_eq
    # 3 - top_raise_with_dicounted_high_eq
    # 4 - top_raise_with_discounted_low_eq
    # 5 - top_raise_with_limit
    # 6 - top_raise_with_limit_discounted_eq  
    # other - top_raise   
  @staticmethod
  def top_card_flop(player, equity, can_raise, can_bet, can_call):
    #debug
    print "--- enter top_card_flop()"

    top_card_band_factor = 1
    # top_strategy_list = [0,0,1,2,2,2,3,4,4,5,6]
    top_strategy_list = [2]
    result = bot_action_lib.BotActionLib.random_get_top_strategy(player, equity, can_raise, can_bet, can_call, top_card_band_factor, top_strategy_list)

    print "--- exit top_card_flop(), result: " + result

    return result 

  @staticmethod
  def top_card_turn(player, equity, can_raise, can_bet, can_call):
    #debug
    print "--- enter top_card_turn()"
    top_card_band_factor = 1
    # top_strategy_list = [1,2,3,5]
    top_strategy_list = [2]
    result = bot_action_lib.BotActionLib.random_get_top_strategy(player, equity, can_raise, can_bet, can_call, top_card_band_factor, top_strategy_list)

    print "--- exit top_card_turn(), result: " + result
        
    return result 

  @staticmethod  
  def top_card_river(player, equity, can_raise, can_bet, can_call):
    #debug
    print "----- enter top_card_river()"

    top_card_band_factor = 1
    # top_strategy_list = [1,1,1,2,2,2,3]
    # try to be the most aggressive here
    top_strategy_list = [1]
    result = bot_action_lib.BotActionLib.random_get_top_strategy(player, equity, can_raise, can_bet, can_call, top_card_band_factor, top_strategy_list)
    print "--- exit top_card_river(), result: " + result
        
    return result        