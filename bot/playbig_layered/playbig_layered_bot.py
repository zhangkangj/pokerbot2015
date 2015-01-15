# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot
from lib.evaluator import evaluator

class Playbig_layeredBot(base_bot.BaseBot):

  def action(self):
    hole_card_str = ''.join(self.player.hole_cards)
    board_card_str = ''.join(self.player.board_cards)
    card_str = hole_card_str+':xx'*(self.player.num_active_player-1)
    equity = evaluator.evaluate(card_str, board_card_str, '', 5000)
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
    return super(Playbig_layeredBot, self).action(equity*0.8, can_raise, can_bet, can_call)

  def preflop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    raise_hand_str = ['AA','KK','QQ','JJ','TT','AK','AQ','AJ','AT','KQ']
    call_hand_str = ['QJ','JT','T9','98','87']
    hole_card_str = ''.join(self.player.hole_cards)
    temp_str1 = hole_card_str[0]+hole_card_str[2]
    temp_str2 = hole_card_str[2]+hole_card_str[0]
    suit_equal = hole_card_str[1] == hole_card_str[3]
    
    if self.player.pot_size > 20:
        if can_call:
            call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
            result = 'CALL:' + str(call_amount)
            print 'calling', result
    else:
        if temp_str1 in raise_hand_str or temp_str2 in raise_hand_str:
            if can_bet:
                result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
                print 'betting', result
            elif can_raise:        
                result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]
                print 'raising', result
            else:
                call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
                result = 'CALL:' + str(call_amount)
                print 'calling', result
        elif suit_equal and (temp_str1 in call_hand_str or temp_str2 in call_hand_str):
            if can_call:
                call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
                if call_amount <= 4:
                    result = 'CALL:' + str(call_amount) 
                    print 'calling', call_amount
                else:
                    result = 'FOLD'
                    print 'folding'
    return result

  def flop(self, equity, can_raise, can_bet, can_call):

    print 'my flop() ................................................. start .................................................'

    result = 'CHECK'
    min_to_bet = 0.5
    min_to_bet_1 = 0.75

    #--Low range
    if equity >= 0 and equity < min_to_bet: 
      # If opponent bets, don't want to follow, have to fold
      if can_call:
        result = 'FOLD' 
      # Otherwise, we just fall back to default 'Check' 
    #--Mid Range
    elif equity >= min_to_bet and equity < min_to_bet_1:
      # Raise based on Equity
      if can_bet:
        bet_legal_act = [action for action in self.player.legal_actions if 'BET' in action][0]
        bet_legal_min = int(bet_legal_act.split(':')[1])
        bet_legal_max = int(bet_legal_act.split(':')[2])
        bet_amount = int(equity * (bet_legal_max - bet_legal_min))
        result = 'BET:' + str(bet_amount)
        print 'betting', bet_amount
      elif can_raise:
        raise_legal_act = [action for action in self.player.legal_actions if 'RAISE' in action][0]
        raise_legal_min = int(raise_legal_act.split(':')[1])
        raise_legal_max = int(raise_legal_act.split(':')[2])
        raise_amount = int(equity * (raise_legal_max - raise_legal_min))
        result = 'RAISE:' + str(raise_amount)
        print 'RAISE', raise_amount
      elif can_call:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount
    #--High Range
    elif equity >= min_to_bet_1 and equity <= 1.0:
      # Raise based on Equity
      if can_bet:
        bet_legal_act = [action for action in self.player.legal_actions if 'BET' in action][0]
        bet_legal_min = int(bet_legal_act.split(':')[1])
        bet_legal_max = int(bet_legal_act.split(':')[2])
        bet_amount = int(equity * (bet_legal_max - bet_legal_min))
        result = 'BET:' + str(bet_amount)
        print 'betting', bet_amount
      elif can_raise:
        raise_legal_act = [action for action in self.player.legal_actions if 'RAISE' in action][0]
        raise_legal_min = int(raise_legal_act.split(':')[1])
        raise_legal_max = int(raise_legal_act.split(':')[2])
        raise_amount = int(equity * (raise_legal_max - raise_legal_min))
        result = 'RAISE:' + str(raise_amount)
        print 'RAISE', raise_amount
      elif can_call:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount

    else:
      print 'ERROR: equity: ', equity, ' is out of legal range'

    print 'my flop() ................................................. end .................................................'

    return result

  def turn(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if can_call:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      if equity * (call_amount + self.player.pot_size) > call_amount:
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount
      else:
        result = 'FOLD'
    return result

  def river(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if can_call:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      if equity * (call_amount + self.player.pot_size) > call_amount:
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount
      else:
        result = 'FOLD'
    return result
