# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: rli
"""

from .. import base_bot
from lib.evaluator import evaluator
# from lib.evaluator import evaluator_cy
from lib import util
import numpy as np
from study.cfr import cfr_cy2



class Base_nashBot(base_bot.BaseBot):
  
  def __init__(self, player, stack = 30, data_= None):
    super(Base_nashBot, self).__init__(player)
    #initialize the bot with corresponding game tree
    self.root = cfr_cy2.RoundNode(0, 0, stack, stack)
    self.last_raise_amount = 0
    self.last_round_pot_size = 0
    #the stack and the data file should match! no check
#    self.root.load_prob(data_)
    self.current_node = self.root
  def action(self):
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
    #Max added the following code to do *
    for action in self.player.last_actions[1:]:
      output = self.move_current_node(action)
      if output == 'Showdown':
        return self.all_in(can_raise, can_bet, can_call)
      elif output == 'Call4bet':
        call_amount = int([action1 for action1 in self.player.legal_actions if 'CALL' in action1][0].split(':')[1])              
        return 'CALL:' + str(call_amount)
      elif output == 'Normal':
        pass
      else:
        print 'impossible output'
        assert 0
        
    #finished evolving nodes, choose action next
    #situation 0:
    if self.current_node.get_node_type() == 'ShowdownNode':
      return self.all_in(can_raise,can_bet,can_call)    
    bucket = self.get_bucket()
    
    print self.current_node.get_node_type(), 'node type yooooooooo', bucket, 'bucket yooooo'
    print self.player.last_actions
    prob = self.current_node.get_act_prob(bucket)
    #draw random number from uniform(0,1), then choose the corresponding node
    r = np.random.uniform(0,1)
    s = 0
    for i in range(0, len(prob)):
      s += prob[i]
      if s >= r:
        index = i
        break
    #chose index as the next action, find call_amount in legal action for later use

    #situation 1:   
    if not can_raise and not can_bet:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])              
      #if can't bet, we should be able to fold-call-raise. If can't raise at the same time. it means the call option means all-in, which means the hand will end after this decision anyway
      if index == 0:
        return 'FOLD'
      else:
        return 'CALL:' + str(call_amount)
    #if not situation 1, get several amount and move node
    raise_amount_min = int([action for action in self.player.legal_actions if ('RAISE' in action or 'BET' in action)][0].split(':')[1])
    raise_amount_max = int([action for action in self.player.legal_actions if ('RAISE' in action or 'BET' in action)][0].split(':')[2])    
    tree_pot_size = self.current_node.get_pot_size()    
    print self.current_node.get_node_type(), 'action node yoooooooooooooo',index
    is_check_node = (self.current_node.get_node_type() == 'CheckNode')
    self.current_node = self.current_node.child_nodes[index]
    #situation 2
    if is_check_node:
      if index == 0:
        return 'CHECK'
      else:          
        tree_raise_ratio = self.current_node.get_raise_amount() / tree_pot_size
        raise_amount_propose = int(tree_raise_ratio * self.player.pot_size)
        raise_amount_final = min(raise_amount_max, max(raise_amount_min, raise_amount_propose))
        print 'bet yooooo:', str(raise_amount_final)
        self.last_raise_amount = raise_amount_final        
        if can_raise:
          return 'RAISE:' + str(raise_amount_final)
        elif can_bet:
          return 'BET:' + str(raise_amount_final)
        else:
          assert 0
          return 'CHECK'
    #situation 3
    else:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])              
      #if not a check node, it has to be a raise node
      if index == 0:
        return 'FOLD'
      elif index == 1:
        return 'CALL:' + str(call_amount)     
      else:
        tree_raise_ratio = self.current_node.get_raise_amount() / tree_pot_size
        #bug, don't know how to get pot_size if call.
        raise_amount_propose = int(tree_raise_ratio * (self.last_round_pot_size + call_amount * 2)) + call_amount
        raise_amount_final = min(raise_amount_max, max(raise_amount_min, raise_amount_propose))
        self.last_raise_amount = raise_amount_final
        return 'RAISE:' + str(raise_amount_final)          
    return super(Base_nashBot, self).action(0, can_raise, can_bet, can_call)
            

  def get_bucket(self):
    mc1, mc2 = util.c2n(self.player.hole_cards)
    if self.player.num_board_card == 0:
      return evaluator_cy.preflop_idx(mc1, mc2)
    elif self.player.num_board_card == 3:
      bc1, bc2, bc3 = util.c2n(self.player.board_cards)
      bucket, _, _  = evaluator.evaluate_flop(mc1, mc2, bc1, bc2, bc3)
      return bucket
    elif self.player.num_board_card == 4:
      bc1, bc2, bc3, bc4 = util.c2n(self.player.board_cards)      
      bucket, _, _  = evaluator.evaluate_turn(mc1, mc2, bc1, bc2, bc3, bc4)
      return bucket
    else:
      assert self.player.num_board_card == 5
      bc1, bc2, bc3, bc4, bc5 = util.c2n(self.player.board_cards)      
      bucket, _ = evaluator.evaluate_river(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
      return bucket

        
  def find_similar_child_node(self, raise_ratios_array, raise_ratio):
    max1 = 1
    j = 0
    for i in range(0,len(raise_ratios_array)):
      if max1 > abs(raise_ratios_array[i] - raise_ratio):
        max1 = abs(raise_ratios_array[i] - raise_ratio)
        j = i
    return j

  def all_in(self, can_raise, can_bet, can_call):
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
  ##################################################################################### 
  def move_current_node(self, action):
    #Max added the following code to do *
    #if we have reached a showdown node, we all in our opponents
    if self.current_node.get_node_type() == 'ShowdownNode':
      return 'Showdown'
    elif action[1] == 'POST':
      print self.current_node.get_node_type(), 'should be maybe roundnode'
      self.current_node = self.root.child_nodes[0]
      self.last_raise_amount = 2
    elif action[1] == 'CALL':
      print self.current_node.get_node_type(), 'should be raise ddddddddddddddddddddddddddd>>>>>>>>>>>>>>>>>>'
      assert self.current_node.get_node_type() == 'RaiseNode'
      self.current_node = self.current_node.child_nodes[1]
      #unfinished
    elif action[1] == 'CHECK':
      print self.current_node.get_node_type(), 'should be check ddddddddddddddddddddddddddd>>>>>>>>>>>>>>>>>>'
      assert self.current_node.get_node_type() == 'CheckNode'
      self.current_node = self.current_node.child_nodes[0]
    elif action[1] == 'DEAL':
      print self.current_node.get_node_type(), 'should be round ddddddddddddddddddddddddddd>>>>>>>>>>>>>>>>>>'
      #check if it is a round node, if not something is wrong, just for dubug perposes
      assert self.current_node.get_node_type() == 'RoundNode'
      self.current_node = self.current_node.child_nodes[0]
      self.last_round_pot_size += 2 * self.last_raise_amount
      self.last_raise_amount = 0
    elif action[1] == 'RAISE' or action[1] == 'BET':
      print self.current_node.get_node_type(), 'should be raise or check ddddddddddddddddddddddddddd>>>>>>>>>>>>>>>>>>'       
      raise_amount = action[2] - self.last_raise_amount
      #compute the ratio of this bet/raise, bug!
      raise_ratio = raise_amount * 1. / (self.last_round_pot_size + 2 * self.last_raise_amount)
      self.last_raise_amount = action[2]
      if self.current_node.get_node_type() == 'CheckNode':
        #if there are raise nodes, find the most similar one
        tree_pot_size = self.current_node.get_pot_size()
        tree_raise_ratios = []
        print self.current_node.get_node_type(), 'current node type'
        for i in range(1,self.current_node.get_num_child()):
          tree_raise_ratios.append(self.current_node.child_nodes[i].get_raise_amount() / tree_pot_size)
        index = self.find_similar_child_node(tree_raise_ratios, raise_ratio)
        self.current_node = self.current_node.child_nodes[index + 1]
      elif self.current_node.get_node_type() == 'RaiseNode':
#        print action[2], self.last_raise_amount, self.current_node.get_num_child()      
        if self.current_node.get_num_child() == 2:
          #if there are only 2 child nodes, it means in the tree there are no raise nodes, only fold and call node
          if self.current_node.child_nodes[1].get_node_type() == 'ShowdownNode':
            #if the call node is a showdown node, it means in the tree we have all_ined, then move to the showndown node, and all in.
            self.current_node = self.current_node.child_nodes[1]
          elif self.current_node.child_nodes[1].get_node_type() == 'RoundNode':
            #if the call node is a round node, it means it has reached the three bets limit in the tree, but the opponent 4 bets, we call and go to the next round node
            self.current_node = self.current_node.child_nodes[1]              
            return 'Call4bet'
          else:
            print 'error'
            assert 0
            return 'Error'
        else:
          #if there are raise nodes, find the most similar one
          tree_pot_size = self.current_node.get_pot_size()
          tree_raise_ratios = []
          for i in range(2,self.current_node.get_num_child()):
            tree_raise_ratios.append(self.current_node.get_raise_amount() / tree_pot_size)
          index = self.find_similar_child_node(tree_raise_ratios, raise_ratio)
          self.current_node = self.current_node.child_nodes[index + 2]
      else:
        print 'wrong node type, should be checknode or raisenode'
        assert 0
        return 'Error'
    else:
      print 'wrong action type'
      assert 0
      return 'Error'
    return 'Normal'  
#####################################################################

  def initialize_from_beginning(self, action_seq):
    for action in action_seq:
      output = self.move_current_node(action)
      if not (output == 'Normal'):
        return False
    if self.current_node.get_node_type() == 'ShowdownNode':
      return False
    else:
      return True
      
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
