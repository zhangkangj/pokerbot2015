# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot
from lib.evaluator import evaluator

class NaiveBot(base_bot.BaseBot):

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
    return super(NaiveBot, self).action(equity*0.8, can_raise, can_bet, can_call)

  def preflop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if can_bet and equity > (1.0/self.player.num_active_player):
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[1]
      print 'betting', result
    elif can_raise and equity > (1.0/self.player.num_active_player):        
      result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]
      print 'raising', result
    elif can_call:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      if equity * (call_amount + self.player.pot_size) > call_amount:
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount
      else:
        result = 'FOLD'
    return result

  def flop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if can_call:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      if equity * (call_amount + self.player.pot_size) > call_amount:
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount
      else:
        result = 'FOLD'
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
