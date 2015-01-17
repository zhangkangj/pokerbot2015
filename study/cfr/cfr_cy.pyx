# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 16:19:06 2015

@author: zhk
"""

import numpy as np
cimport numpy as np

cdef:
  int MAX_BET_NUM = 3
  int TOTAL_STACK = 10

cdef class Node(object):
  cpdef child_nodes
  cpdef utility_sb
  cpdef utility_bb
  
  cdef:
    float* utility_sb_ptr
    float* utility_bb_ptr
    int num_round, num_card_bucket, num_child
    Node[:] child_node_array

  def __init__(self, num_round):
    self.num_round = num_round
    self.num_child = 0
    if num_round == 0:
      self.num_card_bucket = 256
    elif self.num_round == 1:
      self.num_card_bucket = 32
    elif self.num_round == 2:
      self.num_card_bucket = 32
    elif self.num_round == 3:
      self.num_card_bucket = 32
    else:
      self.num_card_bucket = 16
    self.child_nodes = []
  
  def initialize(self):
    cdef:
      np.ndarray[float, ndim=1] utility_sb_ = np.zeros(self.num_card_bucket*self.num_child, dtype=np.float32)
      np.ndarray[float, ndim=1] utility_bb_ = np.zeros(self.num_card_bucket*self.num_child, dtype=np.float32)
    self.utility_sb = utility_sb_
    self.utility_sb_ptr = <float*> utility_sb_.data    
    self.utility_bb = utility_bb_
    self.utility_bb_ptr = <float*> utility_bb_.data

  cdef void spawn_round_node(self, int pot_size, int stack_sb, int stack_bb,
                             int final_amount_sb, int final_amount_bb):
    assert self.num_round >= 0
    node = RoundNode(self.num_round+1, pot_size, stack_sb, stack_bb, final_amount_sb, final_amount_bb)
    self.num_child += 1
    self.child_nodes.append(node)

  cdef void spawn_raise_node(self, int is_sb, int pot_size, int stack_sb, int stack_bb,
                             int amount_sb, int amount_bb,
                             int min_bet, int num_bet, int raise_amount):
    node = RaiseNode(is_sb, self.num_round, pot_size, stack_sb, stack_bb,
                     amount_sb, amount_bb, min_bet, num_bet, raise_amount)
    self.num_child += 1
    self.child_nodes.append(node)

  cdef void spawn_check_node(self, int is_sb, int pot_size, int stack_sb, int stack_bb,
                             int amount_sb, int amount_bb):
    node = CheckNode(is_sb, self.num_round, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    self.num_child += 1
    self.child_nodes.append(node)

  cdef void spawn_fold_node(self, bint sb_win, int pot_size):
    node = FoldNode(sb_win, pot_size)
    self.child_nodes.append(node)
    self.num_child += 1

  cdef void spawn_showdown_node(self, int pot_size):
    node = ShowdownNode(pot_size)
    self.child_nodes.append(node)
    self.num_round += 1

  def traverse(self):
    count = 1
    if self.num_child == 0:
      return count
    else:
      for node in self.child_nodes:
        count += node.traverse()
      return count

  def traverse_game_round(self, game_round):
    count = 0
    if self.num_child == 0:
      return count
    else:
      for node in self.child_nodes:
        count += node.traverse_game_round(game_round)
      return count

  def traverse_round_node(self, game_round):
    count = 0
    if self.num_child == 0:
      return count
    else:
      for node in self.child_nodes:
        count += node.traverse_round_node(game_round)
      return count

'''
  def transit(self, p_sb, p_bb):
    pass
    #return u_sb, u_bb
'''


cdef class RoundNode(Node):
  cdef:
    int preflop_amount_sb, preflop_amount_bb
    int flop_amount_sb, flop_amount_bb
    int turn_amount_sb, turn_amount_bb
    int river_amount_sb, river_amount_bb

  def __init__(self, int num_round, int pot_size, int stack_sb, int stack_bb,
               int amount_sb=0, int amount_bb=0):
    super(RoundNode, self).__init__(num_round)
    assert pot_size + stack_sb + stack_bb + amount_sb + amount_bb == TOTAL_STACK, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    assert pot_size >= 0 and stack_sb >= 0 and stack_bb >= 0 and amount_sb >= 0 and amount_bb >= 0, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    if num_round == 0:
      assert pot_size == 0, ('invalid pot size', pot_size, num_round)
      assert stack_sb == stack_bb
      amount_sb, amount_bb = 1, 2
      self.spawn_raise_node(True, pot_size, stack_sb-1, stack_bb-2,
                            amount_sb, amount_bb, min_bet=2, num_bet=0, raise_amount=2)
    else:
      if num_round - 1 == 0:
        self.preflop_amount_sb = amount_sb
        self.preflop_amount_bb = amount_bb
      elif num_round - 1 == 1:
        self.flop_amount_sb = amount_sb
        self.flop_amount_bb = amount_bb
      elif num_round - 1 == 2:
        self.turn_amount_sb = amount_sb
        self.turn_amount_bb = amount_bb
      # TODO: update values
      self.spawn_check_node(True, pot_size, stack_sb, stack_bb, amount_sb=0, amount_bb=0)
    self.initialize()
    assert len(self.child_nodes) > 0

  def traverse_round_node(self, game_round):
    count = 1 if self.num_round == game_round else 0
    if self.num_child == 0:
      return count
    else:
      for node in self.child_nodes:
        count += node.traverse_round_node(game_round)
      return count
'''
  def transit(self, p_sb, p_bb):
    self.child_nodes[0].transit(p_sb, p_bb)
    self.utility_bb[self.bucket_sequence_bb[self.num_round]] = self.child_nodes[0].utility_bb[self.bucket_sequence_bb[self.num_round]]
    self.utility_sb[self.bucket_sequence_sb[self.num_round]] = self.child_nodes[0].utility_sb[self.bucket_sequence_sb[self.num_round]]
'''


cdef class PlayerNode(Node):
  cpdef regret
  cdef:
    bint is_sb
    float* regret_ptr
    int raise_amount

  def __init__(self, bint is_sb, int num_round):
    self.is_sb = is_sb
    self.raise_amount = 0
    super(PlayerNode, self).__init__(num_round)

  def initialize(self):
    super(PlayerNode, self).initialize()
    cdef:
      np.ndarray[float, ndim=1] regret_ = np.zeros(self.num_card_bucket*self.num_child, dtype=np.float32)
    self.regret = regret_
    self.regret_ptr = <float*> regret_.data     

  def traverse_game_round(self, game_round):
    count = 1 if self.num_round == game_round else 0
    for node in self.child_nodes:
      count += node.traverse_game_round(game_round)
    return count


cdef class RaiseNode(PlayerNode):
  def __init__(self, bint is_sb, int num_round, int pot_size, int stack_sb, int stack_bb,
               int amount_sb, int amount_bb, int min_bet, int num_bet, int raise_amount):
    assert pot_size + stack_sb + stack_bb + amount_sb + amount_bb == TOTAL_STACK, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    assert pot_size >= 0 and stack_sb >= 0 and stack_bb >= 0 and amount_sb >= 0 and amount_bb >= 0, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    super(RaiseNode, self).__init__(is_sb, num_round)
    self.raise_amount = raise_amount
    # player folds
    self.spawn_fold_node(sb_win=(not is_sb), pot_size=pot_size+amount_sb+amount_bb)
    # player calls
    call_amount = abs(amount_bb - amount_sb)
    stack, sb_delta, bb_delta = (stack_sb, call_amount, 0) if is_sb else (stack_bb, 0, call_amount)
    if stack <= call_amount:
      self.spawn_showdown_node(pot_size+amount_sb+amount_bb+call_amount)
    else:
      if num_round < 3:
        # SB calls BB after post blinds
        if num_round == 0 and is_sb and amount_sb == 1 and amount_bb == 2:
          self.spawn_check_node(not is_sb, pot_size, stack_sb-1, stack_bb, amount_sb=2, amount_bb=2)
        else:
        # player calls before river
          self.spawn_round_node(pot_size+amount_sb+amount_bb+call_amount, 
                                stack_sb-sb_delta, stack_bb-bb_delta,
                                final_amount_sb=0, final_amount_bb=0) # TODO: fix final amount
      else:
        # player calls at river
        self.spawn_showdown_node(pot_size+amount_sb+amount_bb+call_amount)
      # player raises
      if num_bet < MAX_BET_NUM:
        raise_limit = stack - call_amount
        # desired_amounts = [min_bet , (pot_size+amount_sb+amount_bb+call_amount)/2, pot_size+amount_sb+amount_bb+call_amount]
        desired_amounts = [(pot_size+amount_sb+amount_bb+call_amount)/2, pot_size+amount_sb+amount_bb+call_amount]
        if raise_limit < pot_size + amount_sb + amount_bb + call_amount:
          raise_amounts = set([amount for amount in desired_amounts if amount < raise_limit] + [raise_limit])
        else:
          raise_amounts = set(desired_amounts)
        for raise_amount in raise_amounts:
          sb_delta_, bb_delta_ = (raise_amount+sb_delta, 0) if is_sb else (0, raise_amount+bb_delta)
          self.spawn_raise_node(not is_sb, pot_size, stack_sb-sb_delta_, stack_bb-bb_delta_,
                                amount_sb+sb_delta_, amount_bb+bb_delta_, raise_amount, num_bet+1, raise_amount)
    self.initialize()

'''
  cdef void transit(self, p_sb, p_bb):
    cdef float* act_prob
    cdef int node_bucket
    act_prob = (float *)malloc(5 * sizeof(float))  
    #update action probablity from regret    
    #traverse tree to compute utilities of child nodes
    if self.active_player == 'SB':
      node_bucket = self.bucket_sequence_sb[self.num_round]
      compute_prob(act_prob, node_bucket)
      for i in range(0, self.num_child):
        self.child_nodes[i].translate(p_sb * act_prob[i], p_bb)
    #compute utility from utilities of child nodes     
      for i in range(0, self.num_child):
        self.utility_sb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_sb[node_bucket]
        self.utility_bb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_bb[node_bucket] 
    #compute new regrets
      for i in range(0, self.num_child):
        self.regret[node_bucket * 5 + i] *= T * 1. / (T + 1)
        self.regret[node_bucket * 5 + i] += p_bb * (self.child_nodes[i].utility_sb[node_bucket] - self.utility_sb[node_bucket]) / (T + 1)
    else:
      node_bucket = self.bucket_sequence_sb[self.num_round]
      compute_prob(act_prob, node_bucket)
      for i in range(0, self.num_child):
        self.child_nodes[i].translate(p_sb, p_bb * act_prob[i])
    #compute utility from utilities of child nodes     
      for i in range(0, self.num_child):
        self.utility_sb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_sb[node_bucket]
        self.utility_bb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_bb[node_bucket]
    #compute new regrets
      for i in range(0, self.num_child):
        self.regret[node_bucket * 5 + i] *= T * 1. / (T + 1)
        self.regret[node_bucket * 5 + i] += p_sb * (self.child_nodes[i].utility_bb[node_bucket] - self.utility_bb[node_bucket]) / (T + 1)
        
  cdef void compute_prob(float* XXX, int node_bucket):
    cdef float sum_regret_plus = 0
    for i in range(0, self.num_child):
      self.regret[node_bucket + i] = max(self.regret[node_bucket + i], 0)
      sum_regret_plus += self.regret[node_bucket + i]
    if sum_regret_plus > 0:
      for i in range(0, self.num_child):
        XXX[i] /= sum_regret_plus
    else:
      tmp = 1./self.num_child
      for i in range(0, self.num_child):
        XXX[i] = tmp
    return
'''

cdef class CheckNode(PlayerNode):

  def __init__(self, bint is_sb, int num_round, int pot_size, int stack_sb, int stack_bb,
               int amount_sb, int amount_bb):
    assert pot_size + stack_sb + stack_bb + amount_sb + amount_bb == TOTAL_STACK, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    assert pot_size >= 0 and stack_sb >= 0 and stack_bb >= 0 and amount_sb >= 0 and amount_bb >= 0, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    super(CheckNode, self).__init__(is_sb, num_round)
    # player checks
    if (num_round == 0 and is_sb) or (num_round > 0 and not is_sb):
      self.spawn_check_node(not is_sb, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    else:
      if num_round == 3:
        assert amount_sb==amount_bb==0
        self.spawn_showdown_node(pot_size)
      else:
        self.spawn_round_node(pot_size+amount_sb+amount_bb, stack_sb, stack_bb,
                              final_amount_sb=0, final_amount_bb=0) # TODO fix final amount
    # player bets
    raise_limit = stack_sb if is_sb else stack_bb
    desired_amounts = [2 , (pot_size+amount_sb+amount_bb)/2, pot_size+amount_sb+amount_bb]
    #desired_amounts = [(pot_size+amount_sb+amount_bb)/2, pot_size+amount_sb+amount_bb]
    if raise_limit < pot_size + amount_sb + amount_bb:
      raise_amounts = set([amount for amount in desired_amounts if amount < raise_limit] + [raise_limit])
    else:
      raise_amounts = set(desired_amounts)
    for raise_amount in raise_amounts:
      sb_delta, bb_delta = (raise_amount, 0) if is_sb else (0, raise_amount)
      self.spawn_raise_node(not is_sb, pot_size, stack_sb-sb_delta, stack_bb-bb_delta,
                            amount_sb+sb_delta, amount_bb+bb_delta, raise_amount, num_bet=1, raise_amount=raise_amount)
    self.initialize()
'''
  cdef void transit(self, p_sb, p_bb):
    cdef float* act_prob
    cdef int node_bucket
    act_prob = (float *)malloc(5 * sizeof(float))  
    #update action probablity from regret    
    #traverse tree to compute utilities of child nodes
    if self.active_player == 'SB':
      node_bucket = self.bucket_sequence_sb[self.num_round]
      compute_prob(act_prob, node_bucket)
      for i in range(0, self.num_child):
        self.child_nodes[i].translate(p_sb * act_prob[i], p_bb)
    #compute utility from utilities of child nodes     
      for i in range(0, self.num_child):
        self.utility_sb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_sb[node_bucket]
        self.utility_bb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_bb[node_bucket] 
    #compute new regrets
      for i in range(0, self.num_child):
        self.regret[node_bucket * 5 + i] *= T * 1. / (T + 1)
        self.regret[node_bucket * 5 + i] += p_bb * (self.child_nodes[i].utility_sb[node_bucket] - self.utility_sb[node_bucket]) / (T + 1)
    else:
      node_bucket = self.bucket_sequence_sb[self.num_round]
      compute_prob(act_prob, node_bucket)
      for i in range(0, self.num_child):
        self.child_nodes[i].translate(p_sb, p_bb * act_prob[i])
    #compute utility from utilities of child nodes     
      for i in range(0, self.num_child):
        self.utility_sb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_sb[node_bucket]
        self.utility_bb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_bb[node_bucket]
    #compute new regrets
      for i in range(0, self.num_child):
        self.regret[node_bucket * 5 + i] *= T * 1. / (T + 1)
        self.regret[node_bucket * 5 + i] += p_sb * (self.child_nodes[i].utility_bb[node_bucket] - self.utility_bb[node_bucket]) / (T + 1)
        
  cdef void compute_prob(float* XXX, int node_bucket):
    cdef float sum_regret_plus = 0
    for i in range(0, self.num_child):
      self.regret[node_bucket + i] = max(self.regret[node_bucket + i], 0)
      sum_regret_plus += self.regret[node_bucket + i]
    if sum_regret_plus > 0:
      for i in range(0, self.num_child):
        XXX[i] /= sum_regret_plus
    else:
      tmp = 1./self.num_child
      for i in range(0, self.num_child):
        XXX[i] = tmp
    return
'''


cdef class FoldNode(Node):
  cdef:
    bint sb_win
    int pot_size

  def __init__(self, bint sb_win, int pot_size):
    self.sb_win = sb_win
    self.pot_size = pot_size
    super(FoldNode, self).__init__(num_round=-1)

cdef class ShowdownNode(Node):
  cdef int pot_size

  def __init__(self, int pot_size):
    self.pot_size = pot_size
    super(ShowdownNode, self).__init__(num_round=-1)
