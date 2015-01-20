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
    self.last_raise_amount = 0
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
      #if we have reached a showdown node, we all in our opponents
      if self.current_node.get_node_type() == 'ShowdownNode':
        return self.all_in()
      elif action[1] == 'POST':
        self.current_node = self.root
        self.last_raise_amount = 2
      elif action[1] == 'CALL':
        assert self.current_node.get_node_type() == 'RaiseNode'
        self.current_node = self.current_node.child_nodes[1]
      elif action[1] == 'CHECK':
        assert self.current_node.get_node_type() == 'CheckNode'
        self.current_node = self.current_node.child_nodes[0]
      elif action[1] == 'DEAL':
        #check if it is a round node, if not something is wrong, just for dubug perposes
        assert self.current_node.get_node_type() == 'RoundNode'
        self.current_node = self.current_node.child_nodes[0]
        self.last_raise_amount = 0
      elif action[1] == 'RAISE' or action[1] == 'BET':
        raise_amount = action[2] - self.last_raise_amount
        self.last_raise_amount = action[2]
        #compute the ratio of this bet/raise
        raise_ratio = raise_amount * 1. / self.player.pot_size
        if self.current_node.get_node_type() == 'CheckNode':
          #if there are raise nodes, find the most similar one
          tree_pot_size = self.current_node.get_pot_size()
          tree_raise_ratios = []
          for i in range(1,self.current_node.num_child):
            tree_raise_ratios.append(self.current_node.get_raise_amount() / tree_pot_size)
          index = find_similar_child_node(tree_raise_ratio, raise_ratio)
          self.current_node = self.current_node.child_nodes[index + 1]
        elif self.current_node.get_node_type() == 'RaiseNode':
          if self.current_node.num_child == 2:
            #if there are only 2 child nodes, it means in the tree there are no raise nodes, only fold and call node
            if self.current_node.child_nodes[1].get_node_type() == 'ShowdownNode':
              #if the call node is a showdown node, it means in the tree we have all_ined, then move to the showndown node, and all in.
              self.current_node = self.current_node.child_nodes[1]
            elif self.current_node.child_nodes[1].get_node_type() == 'RoundNode':
              #if the call node is a round node, it means it has reached the three bets limit in the tree, but the opponent 4 bets, we call and go to the next round node
              self.current_node = self.current_node.child_nodes[1]              
              call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])              
              return 'CALL:' + str(call_amount)
            else:
              print 'error'
              return 'CHECK'
          else:
            #if there are raise nodes, find the most similar one
            tree_pot_size = self.current_node.get_pot_size()
            tree_raise_ratios = []
            for i in range(2,self.current_node.num_child):
              tree_raise_ratios.append(self.current_node.get_raise_amount() / tree_pot_size)
            index = find_similar_child_node(tree_raise_ratio, raise_ratio)
            self.current_node = self.current_node.child_nodes[index + 2]
        else:
          print 'wrong node type'
          return 'CHECK'
    #finished evolving nodes, choose action next
    bucket = evaluator...
    prob = self.current_node.get_act_prob(bucket)
    r = np.random.uniform(0,1)
    s = 0
    for i in range(0, len(prob)):
      s += prob(i)
      if s >= r:
        index = i
        break
    #chose index as the next action, move node
    tree_pot_size = self.current_node.get_pot_size()
    self.current_node = self.current_node.child_nodes[index]
    #legalize the action
    tree_raise_ratio = self.current_node.get_raise_amount() / tree_pot_size
    #XXX
    
    
        
        
    return super(Base_nashBot, self).action(0, can_raise, can_bet, can_call)
            
          
  def find_similar_child_node(raise_ratios_array, raise_ratio):
    max1 = 1
    j = 0
    for i in range(0,len(raise_ratios_array)):
      if max1 > abs(raise_ratios_array - raise_ratio):
        max1 = abs(raise_ratios_array - raise_ratio)
        j = i
    return j

  def all_in(self):
    if can_bet:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
        print 'betting', result
    elif can_raise:        
      result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]
      print 'raising', result
    elif can_call:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)
      print 'calling', result
    else:
      print 'something is wrong!!!For a raise-able hand: cannot bet, raise, or call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK'
      result = 'CHECK'
    return result  
    
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
