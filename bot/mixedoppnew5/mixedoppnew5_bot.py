# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot
from lib.evaluator import evaluator

import bot_action_lib
import top_play_lib

class Mixedoppnew5Bot(base_bot.BaseBot):

  def action(self):
    hole_card_str = ''.join(self.player.hole_cards)
    board_card_str = ''.join(self.player.board_cards)
    card_str = hole_card_str+':xx'*(self.player.num_active_player-1)
    equity = evaluator.evaluate(card_str, board_card_str, '', 300)
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
    return super(Mixedoppnew5Bot, self).action(equity, can_raise, can_bet, can_call)

  def preflop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    raise_hand_str = ['AA','KK','QQ','JJ','TT','AK','AQ','AJ','AT','KQ']
    suited_call_hand_str = ['QJ','JT','T9','98','87']
    low_call_hand_str = ['KJ','QJ','JT','99','88','77']
    very_low_call_hand_str = ['QT', 'Q9', '66', '55']

    hole_card_str = ''.join(self.player.hole_cards)
    temp_str1 = hole_card_str[0]+hole_card_str[2]
    temp_str2 = hole_card_str[2]+hole_card_str[0]
    suit_equal = hole_card_str[1] == hole_card_str[3]
    
    is_raise_hand = (temp_str1 in raise_hand_str or temp_str2 in raise_hand_str)
    is_suited_call_hand = (suit_equal and (temp_str1 in suited_call_hand_str or temp_str2 in suited_call_hand_str))
    is_low_call_hand = (temp_str1 in low_call_hand_str or temp_str2 in low_call_hand_str)
    is_very_low_call_hand = (temp_str1 in very_low_call_hand_str or temp_str2 in very_low_call_hand_str)

    #debug
    print "----------look at the hole_cards: " + str(hole_card_str) 
    print "----------FLAGS: is_raise_hand: " + str(is_raise_hand) + ", is_suited_call_hand: " + str(is_suited_call_hand) + ", is_low_call_hand" + str(is_low_call_hand)
    print "----------equity: " + str(equity)
    print "----------curr pot_size: " + str(self.player.pot_size) 

    preflop_raisehand_raise_limit = 20
    preflop_suitedcallhand_call_limit = 4
    preflop_lowcallhand_call_limit = 2
    preflop_verylowcallhand_call_limit = 2
    preflop_nogoodhand_call_limit = 2

    if is_raise_hand:
        #debug
        print "----------## enter is_raise_hand, max raise, no call preflop_raisehand_raise_limit:" + str(preflop_raisehand_raise_limit)
        result = bot_action_lib.BotActionLib.action_equity_raise_call_max(self.player, equity, can_raise, can_bet, can_call, 1, preflop_raisehand_raise_limit, None)  
    elif is_suited_call_hand:
        #debug
        print "----------## enter is_suited_call_hand, call with preflop_suitedcallhand_call_limit:" + str(preflop_suitedcallhand_call_limit)
        result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, preflop_suitedcallhand_call_limit)       
    elif is_low_call_hand:
        #debug
        print "----------## enter is_low_call_hand, call with preflop_lowcallhand_call_limit:" + str(preflop_lowcallhand_call_limit)
        result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, preflop_lowcallhand_call_limit)
    elif is_very_low_call_hand:
        #debug
        print "----------## enter is_very_low_call_hand, call with preflop_lowcallhand_call_limit:" + str(preflop_lowcallhand_call_limit)
        result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, preflop_verylowcallhand_call_limit)
    elif can_call:
        #debug
        print "----------## enter no good hand can_call, call with preflop_nogoodhand_call_limit:" + str(preflop_nogoodhand_call_limit)         
        result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, preflop_nogoodhand_call_limit)
    else:
        print 'For a no good card hand: cannot call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK'

    print "----------## exiting preflop..., result:" + str(result)

    return result

  def low_card(self, equity, can_raise, can_bet, can_call):
    #debug
    print "--------> enter low_card()"

    result = 'CHECK'

    if can_call:
      # If opponent bets, don't want to follow, have to fold
      result = 'FOLD' 
    # Otherwise, we just fall back to default 'Check' 
    return result

  def mid_card_river(self, equity, can_raise, can_bet, can_call):
    # unlike high card, for mid card, at river, we should play more conservatively

    result = 'CHECK'
    #debug
    print "--------> enter mid_card_river()"

    call_limit_factor = 0.5

    equity_band_factor = 1
    call_limit = self.player.current_stacksize * equity * call_limit_factor

    # at river you know that for sure you only have a mid hand, play conservatively with lower call limit
    result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, call_limit)
    
    # equity_band_factor = 1
    # call_limit = self.player.current_stacksize * 0.2
    # mid_card_toraise_limit = self.player.game_init_stack_size * 1
    # if self.player.current_stacksize < mid_card_toraise_limit:
    #     result = bot_action_lib.BotActionLib.action_equity_call_fold(equity, can_raise, can_bet, can_call, call_limit)
    # else:   
    #     raise_limit = self.player.current_stacksize - mid_card_toraise_limit
    #     result = bot_action_lib.BotActionLib.action_equity_raise_call(equity, can_raise, can_bet, can_call, equity_band_factor, raise_limit, call_limit)   
    
    #debug
    print "--------> exit mid_card_river(), result:" + result
    return result

  def mid_card(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    #debug
    print "--------> enter mid_card()"

    call_limit_factor = 1.0

    equity_band_factor = 1
    call_limit = self.player.current_stacksize * equity * call_limit_factor

    # call with a limit to leave room to improve
    result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, call_limit)

    # mid_card_toraise_limit = self.player.game_init_stack_size * 1

    # if self.player.current_stacksize < mid_card_toraise_limit:
    #     result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, call_limit)
    # else:   
    #     raise_limit = self.player.current_stacksize - mid_card_toraise_limit
    #     result = bot_action_lib.BotActionLib.action_equity_raise_call(self.player, equity, can_raise, can_bet, can_call, equity_band_factor, raise_limit, call_limit)   
    
    #debug
    print "--------> exit mid_card(), result:" + result
    
    return result

  def high_card(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    #debug
    print "--------> enter high_card()"

    equity_band_factor = 1

    # raise_limit = self.player.current_stacksize * 0.3
    # call_limit = self.player.current_stacksize * 0.6

    raise_limit_factor = 0.5

    call_limit = None
    # use a raise limit to reduce loss if we end up losing, given this is not the 'top' card spectrum 
    raise_limit = self.player.current_stacksize * equity * raise_limit_factor

    result = bot_action_lib.BotActionLib.action_equity_raise_call(self.player, equity, can_raise, can_bet, can_call, equity_band_factor, raise_limit, call_limit)   
    
    return result 

  def high_card_river(self, equity, can_raise, can_bet, can_call):
    # unlike mid card, for high card, at river, we should play more agressively

    result = 'CHECK'
    #debug
    print "--------> enter high_card()"

    equity_band_factor = 1

    # raise_limit = self.player.current_stacksize * 0.4
    # call_limit = self.player.current_stacksize * 0.8

    raise_limit_factor = 1.0

    call_limit = None
    # use a raise limit to reduce loss if we end up losing, given this is not the 'top' card spectrum 
    raise_limit = self.player.current_stacksize * equity * raise_limit_factor

    result = bot_action_lib.BotActionLib.action_equity_raise_call(self.player, equity, can_raise, can_bet, can_call, equity_band_factor, raise_limit, call_limit)   
    
    return result 

  def flop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    #debug
    print "------> enter flop(), equity:" + str(equity)

    # maximum percentage we should discount the equity for opponent observing result
    # base_max_discount_factor_for_opponent = 0.4
    # if equity > 0.95:
    #   max_discount_factor_for_opponent = 0.25 * base_max_discount_factor_for_opponent
    # elif equity > 0.9:
    #   max_discount_factor_for_opponent = 0.5 * base_max_discount_factor_for_opponent
    # else:
    #   max_discount_factor_for_opponent = 1 * base_max_discount_factor_for_opponent

    max_discount_factor_for_opponent = 0.05
    equity = self.player.discount_equity_for_opponent(equity, max_discount_factor_for_opponent)

    #result = 'CHECK'
    min_to_bet_mid = 0.4
    min_to_bet_high = 0.7
    min_to_bet_top = 0.8

    # maximum percentage we should discount the equity for opponent observing result
    # base_max_discount_factor_for_opponent = 0.4
    # if equity > 0.95:
    #   # care less about the opponents if we have really good cards
    #   max_discount_factor_for_opponent = 0.25 * base_max_discount_factor_for_opponent
    # elif equity > 0.9:
    #   max_discount_factor_for_opponent = 0.5 * base_max_discount_factor_for_opponent
    # else:
    #   max_discount_factor_for_opponent = 1 * base_max_discount_factor_for_opponent

    if equity < min_to_bet_top:
        print "------> flop(), equity:" + str(equity) + " is less than top card equity, needs discount by observing opponents."
        equity = self.player.discount_equity_for_opponent(equity, max_discount_factor_for_opponent)
    else:
        print "------> flop(), equity:" + str(equity) + " is greater than top card equity, ignore opponents action."


    #--Low range
    if equity < min_to_bet_mid: 
      result = self.low_card(equity, can_raise, can_bet, can_call)
    #--Mid Range
    elif equity >= min_to_bet_mid and equity < min_to_bet_high:
      result = self.mid_card(equity, can_raise, can_bet, can_call)
    #--High Range
    elif equity >= min_to_bet_high and equity <= min_to_bet_top:
      result = self.high_card(equity, can_raise, can_bet, can_call)
    #--Top Range
    else:
      result = top_play_lib.TopPlayLib.top_card_flop(self.player, equity, can_raise, can_bet, can_call)
    return result

  def turn(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    #debug
    print "------> enter turn(), equity:" + str(equity)

    #result = 'CHECK'
    min_to_bet_mid = 0.5
    min_to_bet_high = 0.725
    min_to_bet_top = 0.825
    max_discount_factor_for_opponent = 0.075

    # maximum percentage we should discount the equity for opponent observing result
    # base_max_discount_factor_for_opponent = 0.4
    # if equity > 0.95:
    #   # care less about the opponents if we have really good cards
    #   max_discount_factor_for_opponent = 0.25 * base_max_discount_factor_for_opponent
    # elif equity > 0.9:
    #   max_discount_factor_for_opponent = 0.5 * base_max_discount_factor_for_opponent
    # else:
    #   max_discount_factor_for_opponent = 1 * base_max_discount_factor_for_opponent

    if equity < min_to_bet_top:
        print "------> turn(), equity:" + str(equity) + " is less than top card equity, needs discount by observing opponents."
        equity = self.player.discount_equity_for_opponent(equity, max_discount_factor_for_opponent)
    else:
        print "------> turn(), equity:" + str(equity) + " is greater than top card equity, ignore opponents action."

    #--Low range
    if equity < min_to_bet_mid: 
      result = self.low_card(equity, can_raise, can_bet, can_call)
    #--Mid Range
    elif equity >= min_to_bet_mid and equity < min_to_bet_high:
      result = self.mid_card(equity, can_raise, can_bet, can_call)
    #--High Range
    elif equity >= min_to_bet_high and equity <= min_to_bet_top:
      result = self.high_card(equity, can_raise, can_bet, can_call)
    #--Top Range
    else:
      result = top_play_lib.TopPlayLib.top_card_turn(self.player, equity, can_raise, can_bet, can_call)

    return result

  def river(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'

    #debug
    print "------> enter river(), equity:" + str(equity)

    # medium top pair: 0.548
    # bash-3.2$  ./calculator.sh tdkc:xx:xx 4d7h2sjdts
    # [('tdkc', 0.5483333333333333), ('xx', 0.26), ('xx', 0.19166666666666668)]   

    # high top pair: 0.723
    # bash-3.2$  ./calculator.sh tdac:xx:xx 4d7h2sad9s
    # [('tdac', 0.7233333333333334), ('xx', 0.15), ('xx', 0.12666666666666668)]

    # medium set: 0.916
    # bash-3.2$ ./calculator.sh td6c:xx:xx 4dthjs5dts
    # [('td6c', 0.9166666666666666), ('xx', 0.03166666666666667), ('xx', 0.051666666666666666)]

    #result = 'CHECK'
    min_to_bet_mid = 0.5
    min_to_bet_high = 0.75
    min_to_bet_top = 0.85
    max_discount_factor_for_opponent = 0.1

    # maximum percentage we should discount the equity for opponent observing result
    # base_max_discount_factor_for_opponent = 0.4
    # if equity > 0.95:
    #   # care less about the opponents if we have really good cards
    #   max_discount_factor_for_opponent = 0.25 * base_max_discount_factor_for_opponent
    # elif equity > 0.9:
    #   max_discount_factor_for_opponent = 0.5 * base_max_discount_factor_for_opponent
    # else:
    #   max_discount_factor_for_opponent = 1 * base_max_discount_factor_for_opponent

    if equity < min_to_bet_top:
        print "------> river(), equity:" + str(equity) + " is less than top card equity, needs discount by observing opponents."
        equity = self.player.discount_equity_for_opponent(equity, max_discount_factor_for_opponent)
    else:
        print "------> river(), equity:" + str(equity) + " is greater than top card equity, ignore opponents action."

    #--Low range
    if equity < min_to_bet_mid: 
      result = self.low_card(equity, can_raise, can_bet, can_call)
    #--Mid Range
    elif equity >= min_to_bet_mid and equity < min_to_bet_high:
      result = self.mid_card_river(equity, can_raise, can_bet, can_call)
    #--High Range
    elif equity >= min_to_bet_high and equity <= min_to_bet_top:
      result = self.high_card_river(equity, can_raise, can_bet, can_call)
    #--Top Range
    else:
      result = top_play_lib.TopPlayLib.top_card_river(self.player, equity, can_raise, can_bet, can_call)

    return result

