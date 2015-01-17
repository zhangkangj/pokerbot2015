# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: rli
"""

from .. import base_bot
from lib.evaluator import evaluator

class Base_nashBot(base_bot.BaseBot):

  def action(self):
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
    return super(Base_nashBot, self).action(0, can_raise, can_bet, can_call)

  def preflop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if can_call:
      result = 'FOLD'
    return result

  def flop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if can_call:
      result = 'FOLD'
    return result

  def turn(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if can_call:
      result = 'FOLD'
    return result

  def river(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if can_call:
      result = 'FOLD'
    return result
