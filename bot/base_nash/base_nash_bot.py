# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: rli
"""

from .. import base_bot
from lib.evaluator import evaluator

import numpy as np
from study.cfr import cfr_cy2



class Base_nashBot(base_bot.BaseBot):
  
  def __init__(self, player, stack = 30, data_= None):
    super(Base_nashBot, self).__init__(player)
    #initialize the bot with corresponding game tree
    self.root = cfr_cy2.RoundNode(0, 0, stack, stack)
    #the stack and the data file should match! no check
#    self.root.load_prob(data_)
#    self.current_node = self.root
  def action(self):
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
    #Max added the following code to do *
    
    
    for action in self.player.last_actions:
      if action[1] == 'POST':
        self.current_node = self.root
      elif action[1] == 'CALL':
        
        self.current_node.
      print action, 'this is action'
#        
#    
    
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
