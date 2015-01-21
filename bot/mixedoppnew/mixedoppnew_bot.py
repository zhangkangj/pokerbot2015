# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot
from lib.evaluator import evaluator

import bot_action_lib
import top_play_lib

class MixedoppnewBot(base_bot.BaseBot):

  def action(self):
    hole_card_str = ''.join(self.player.hole_cards)
    board_card_str = ''.join(self.player.board_cards)
    card_str = hole_card_str+':xx'*(self.player.num_active_player-1)
    equity = evaluator.evaluate(card_str, board_card_str, '', 500)
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
    return super(MixedoppnewBot, self).action(equity*0.8, can_raise, can_bet, can_call)

  def preflop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    raise_hand_str = ['AA','KK','QQ','JJ','TT','AK','AQ','AJ','AT','KQ']
    call_hand_str = ['QJ','JT','T9','98','87']
    hole_card_str = ''.join(self.player.hole_cards)
    temp_str1 = hole_card_str[0]+hole_card_str[2]
    temp_str2 = hole_card_str[2]+hole_card_str[0]
    suit_equal = hole_card_str[1] == hole_card_str[3]
    
    is_raise_hand = (temp_str1 in raise_hand_str or temp_str2 in raise_hand_str)
    is_call_hand = (suit_equal and (temp_str1 in call_hand_str or temp_str2 in call_hand_str))

    #debug
    print "----------look at the hole_cards: " + str(hole_card_str) 
    print "----------FLAGS: is_raise_hand: " + str(is_raise_hand) + ", is_call_hand: " + str(is_call_hand) 
    print "----------equity: " + str(equity)
    print "----------curr pot_size: " + str(self.player.pot_size) 

    preflop_raisehand_raise_limit = 20
    preflop_callhand_call_limit = 4

    preflop_nogoodhand_call_limit = 4

    if is_raise_hand:
        #debug
        print "----------## enter is_raise_hand, max raise, no call limit"

        result = bot_action_lib.BotActionLib.action_equity_raise_call_max(self.player, equity, can_raise, can_bet, can_call, 1, preflop_raisehand_raise_limit, None)  
    elif is_call_hand:
        #debug
        print "----------## enter is_can_hand, call with limit"
      
        result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, preflop_callhand_call_limit)       
    elif can_call:
        #debug
        print "----------## enter no good hand can_call, call with very small limit"          
        result = bot_action_lib.BotActionLib.action_equity_call_fold(self.player, equity, can_raise, can_bet, can_call, preflop_nogoodhand_call_limit)
    else:
        print 'For a no good card hand: cannot call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK'

    print "----------## exiting preflop..., result:" + str(result)

    return result


  def low_card(self, equity, can_raise, can_bet, can_call):
    #debug
    print "--------> enter low_card()"

    result = 'CHECK'
    # If opponent bets, don't want to follow, have to fold
    if can_call:
      result = 'FOLD' 
    # Otherwise, we just fall back to default 'Check' 
    return result

  def mid_card_river(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    #debug
    print "--------> enter mid_card_river()"

    equity_band_factor = 1
    call_limit = self.player.current_stacksize * 0.2

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
    equity_band_factor = 1
    call_limit = self.player.current_stacksize * 0.4

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

    raise_limit = self.player.current_stacksize * 0.3
    call_limit = self.player.current_stacksize * 0.6

    result = bot_action_lib.BotActionLib.action_equity_raise_call(self.player, equity, can_raise, can_bet, can_call, equity_band_factor, raise_limit, call_limit)   
    
    return result 

  def high_card_river(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    #debug
    print "--------> enter high_card()"

    equity_band_factor = 1

    raise_limit = self.player.current_stacksize * 0.4
    call_limit = self.player.current_stacksize * 0.8

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
    min_to_bet_mid = 0.5
    min_to_bet_high = 0.7
    min_to_bet_top = 0.8

    #--Low range
    if equity < min_to_bet_mid: 
      result = self.low_card(equity, can_raise, can_bet, can_call)
    #--Mid Range
    elif equity >= min_to_bet_mid and equity < min_to_bet_high:
      result = self.mid_card_river(equity, can_raise, can_bet, can_call)
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

    # maximum percentage we should discount the equity for opponent observing result
    # base_max_discount_factor_for_opponent = 0.4
    # if equity > 0.95:
    #   max_discount_factor_for_opponent = 0.25 * base_max_discount_factor_for_opponent
    # elif equity > 0.9:
    #   max_discount_factor_for_opponent = 0.5 * base_max_discount_factor_for_opponent
    # else:
    #   max_discount_factor_for_opponent = 1 * base_max_discount_factor_for_opponent

    max_discount_factor_for_opponent = 0.15
    equity = self.player.discount_equity_for_opponent(equity, max_discount_factor_for_opponent)

    #result = 'CHECK'
    min_to_bet_mid = 0.5
    min_to_bet_high = 0.75
    min_to_bet_top = 0.85

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

    # maximum percentage we should discount the equity for opponent observing result
    # base_max_discount_factor_for_opponent = 0.4
    # if equity > 0.95:
    #   max_discount_factor_for_opponent = 0.25 * base_max_discount_factor_for_opponent
    # elif equity > 0.9:
    #   max_discount_factor_for_opponent = 0.5 * base_max_discount_factor_for_opponent
    # else:
    #   max_discount_factor_for_opponent = 1 * base_max_discount_factor_for_opponent

    max_discount_factor_for_opponent = 0.2
    equity = self.player.discount_equity_for_opponent(equity, max_discount_factor_for_opponent)

    #result = 'CHECK'
    min_to_bet_mid = 0.5
    min_to_bet_high = 0.8
    min_to_bet_top = 0.95

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

