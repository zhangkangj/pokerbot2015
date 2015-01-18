# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 16:19:06 2015

@author: zhk
"""

import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free


cdef:
  int MAX_BET_NUM = 3
  int TOTAL_STACK = 4

cdef class Node(object):
  cpdef public child_nodes
  #cpdef public utility_sb
  #cpdef public utility_bb
  
  cdef:
    #float* utility_sb_ptr
    #float* utility_bb_ptr
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
      self.num_card_bucket = 8
    self.child_nodes = []
  
#  def initialize(self):
#    cdef:
#      np.ndarray[float, ndim=1] utility_sb_ = np.zeros(self.num_card_bucket*self.num_child, dtype=np.float32)
#      np.ndarray[float, ndim=1] utility_bb_ = np.zeros(self.num_card_bucket*self.num_child, dtype=np.float32)
#    self.utility_sb = utility_sb_
#    self.utility_sb_ptr = <float*> utility_sb_.data    
#    self.utility_bb = utility_bb_
#    self.utility_bb_ptr = <float*> utility_bb_.data

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

  cdef void spawn_fold_node(self, bint sb_win, int win_amount):
    node = FoldNode(sb_win, win_amount)
    self.child_nodes.append(node)
    self.num_child += 1

  cdef void spawn_showdown_node(self, int pot_size):
    node = ShowdownNode(pot_size)
    self.child_nodes.append(node)
    self.num_child += 1

  def traverse(self, game_round):
    total_count = 1 if self.num_round == game_round else 0
    round_count = 0
    raise_count = 0
    check_count = 0
    if self.num_child == 0:
      return total_count, round_count, raise_count, check_count
    else:
      for node in self.child_nodes:
        a, b, c, d = node.traverse()
        total_count += a
        round_count += b
        raise_count += c
        check_count += d        
      return total_count, round_count, raise_count, check_count

  def test_transit(self):
    cdef:
      np.ndarray[int, ndim=1] bucket_seq_sb = np.zeros(5, dtype=np.int32)
      np.ndarray[int, ndim=1] bucket_seq_bb = np.zeros(5, dtype=np.int32)
      np.ndarray[float, ndim=1] util_sb = np.zeros(1, dtype=np.float32)
      np.ndarray[float, ndim=1] util_bb = np.zeros(1, dtype=np.float32)
      float* util_sb_ptr = <float*> util_sb.data
      float* util_bb_ptr = <float*> util_bb.data
      int* bucket_seq_sb_ptr = <int*> bucket_seq_sb.data
      int* bucket_seq_bb_ptr = <int*> bucket_seq_bb.data
    self.transit(0, 0, util_sb_ptr, util_bb_ptr, bucket_seq_sb_ptr, bucket_seq_bb_ptr)
        
  cdef void transit(self, float p_sb, float p_bb, float* util_sb, float* util_bb,
                    int* bucket_seq_sb, int* bucket_seq_bb):
    pass

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
    # self.initialize()
    assert len(self.child_nodes) > 0

  def traverse(self, game_round):
    total_count = 1 if self.num_round == game_round else 0
    round_count = 1 if self.num_round == game_round else 0
    raise_count = 0
    check_count = 0
    if self.num_child != 0:
      for node in self.child_nodes:
        a, b, c, d = node.traverse(game_round)
        total_count += a
        round_count += b
        raise_count += c
        check_count += d        
    return total_count, round_count, raise_count, check_count

  cdef void transit(self, float p_sb, float p_bb, float* util_sb, float* util_bb,
                    int* bucket_seq_sb, int* bucket_seq_bb):
    cdef:
      Node node = <Node> self.child_nodes[0]
    node.transit(p_sb, p_bb, util_sb, util_bb, bucket_seq_sb, bucket_seq_bb)


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
    # super(PlayerNode, self).initialize()
    cdef:
      np.ndarray[float, ndim=1] regret_ = np.zeros(self.num_card_bucket*self.num_child, dtype=np.float32)
    self.regret = regret_
    self.regret_ptr = <float*> regret_.data     

  cdef void transit(self, float p_sb, float p_bb, float* util_sb, float* util_bb,
                    int* bucket_seq_sb, int* bucket_seq_bb):
    cdef float* act_prob = <float*> malloc(self.num_child * sizeof(float))  
    cdef float* util_sb_child = <float*> malloc(self.num_child * sizeof(float))  
    cdef float* util_bb_child = <float*> malloc(self.num_child * sizeof(float))
    cdef int node_bucket, i
    cdef Node node
    #update action probablity from regret    
    #traverse tree to compute utilities of child nodes
    if self.is_sb:
      node_bucket = self.bucket_sequence_sb[self.num_round]
      self.compute_prob(act_prob, node_bucket*self.num_child)
      for i in range(0, self.num_child):
        node = <Node> self.child_nodes[i]
        node.transit(p_sb * act_prob[i], p_bb, 
                     util_sb_child + i, util_bb_child + i, bucket_seq_sb, bucket_seq_bb)
    #compute utility from utilities of child nodes     
      for i in range(0, self.num_child):
        util_sb[0] = act_prob[i] * util_sb_child[i]
        util_bb[0] = act_prob[i] * util_bb_child[i]
    #compute new regrets
      for i in range(0, self.num_child):
        self.regret_ptr[node_bucket * self.num_child + i] += p_bb * (util_sb_child[i] - util_sb[0])
    else:
      node_bucket = self.bucket_sequence_bb[self.num_round]
      self.compute_prob(act_prob, node_bucket*self.num_child)
      for i in range(0, self.num_child):
        node = <Node> self.child_nodes[i]
        node.transit(p_sb, p_bb * act_prob[i], 
                     util_sb_child + i, util_bb_child + i, bucket_seq_sb, bucket_seq_bb)
      #compute utility from utilities of child nodes     
      for i in range(0, self.num_child):
        util_sb[0] = act_prob[i] * util_sb_child[i]
        util_bb[0] = act_prob[i] * util_bb_child[i]
      #compute new regrets
      for i in range(0, self.num_child):
        self.regret_ptr[node_bucket * self.num_child + i] += p_sb * (util_bb_child[i] - util_bb[0])
    free(act_prob)
    free(util_sb_child)
    free(util_bb_child)

  cdef void compute_prob(self, float* result, int node_bucket_times_num_child):
    cdef float sum_regret_plus = 0
    cdef int i
    for i in range(0, self.num_child):
      result[i] = max(self.regret_ptr[node_bucket_times_num_child + i], 0)
      sum_regret_plus += result[i]
    if sum_regret_plus > 0:
      for i in range(0, self.num_child):
        result[i] /= sum_regret_plus
    else:
      for i in range(0, self.num_child):
        result[i] = 1./self.num_child


cdef class RaiseNode(PlayerNode):
  def __init__(self, bint is_sb, int num_round, int pot_size, int stack_sb, int stack_bb,
               int amount_sb, int amount_bb, int min_bet, int num_bet, int raise_amount):
    assert pot_size + stack_sb + stack_bb + amount_sb + amount_bb == TOTAL_STACK, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    assert pot_size >= 0 and stack_sb >= 0 and stack_bb >= 0 and amount_sb >= 0 and amount_bb >= 0, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    super(RaiseNode, self).__init__(is_sb, num_round)
    self.raise_amount = raise_amount
    # player folds
    self.spawn_fold_node(sb_win=(not is_sb), win_amount=(pot_size/2+min(amount_sb, amount_bb)))
    # player calls
    cdef:
      int stack, sb_delta=0, bb_delta=0, call_amount
    if is_sb:
      stack = stack_sb
      call_amount = amount_bb - amount_sb
      sb_delta = call_amount
    else:
      stack = stack_bb
      call_amount = amount_sb - amount_bb
      bb_delta = call_amount
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
        #desired_amounts = [(pot_size+amount_sb+amount_bb+call_amount)/3, (pot_size+amount_sb+amount_bb+call_amount)*2/3, pot_size+amount_sb+amount_bb+call_amount]
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

  def traverse(self, game_round):
    total_count = 1 if self.num_round == game_round else 0
    round_count = 0
    raise_count = 1 if self.num_round == game_round else 0
    check_count = 0
    if self.num_child != 0:
      for node in self.child_nodes:
        a, b, c, d = node.traverse(game_round)
        total_count += a
        round_count += b
        raise_count += c
        check_count += d        
    return total_count, round_count, raise_count, check_count


cdef class CheckNode(PlayerNode):

  def __init__(self, bint is_sb, int num_round, int pot_size, int stack_sb, int stack_bb,
               int amount_sb, int amount_bb):
    assert pot_size + stack_sb + stack_bb + amount_sb + amount_bb == TOTAL_STACK, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    assert pot_size >= 0 and stack_sb >= 0 and stack_bb >= 0 and amount_sb >= 0 and amount_bb >= 0, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    super(CheckNode, self).__init__(is_sb, num_round)
    # player checks
    if is_sb:
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
    if raise_limit < pot_size + amount_sb + amount_bb:
      raise_amounts = set([amount for amount in desired_amounts if amount < raise_limit] + [raise_limit])
    else:
      raise_amounts = set(desired_amounts)
    for raise_amount in raise_amounts:
      sb_delta, bb_delta = (raise_amount, 0) if is_sb else (0, raise_amount)
      self.spawn_raise_node(not is_sb, pot_size, stack_sb-sb_delta, stack_bb-bb_delta,
                            amount_sb+sb_delta, amount_bb+bb_delta, raise_amount, num_bet=1, raise_amount=raise_amount)
    self.initialize()


  def traverse(self, game_round):
    total_count = 1 if self.num_round == game_round else 0
    round_count = 0
    raise_count = 0
    check_count = 1 if self.num_round == game_round else 0
    if self.num_child != 0:
      for node in self.child_nodes:
        a, b, c, d = node.traverse(game_round)
        total_count += a
        round_count += b
        raise_count += c
        check_count += d        
    return total_count, round_count, raise_count, check_count


cdef class FoldNode(Node):
  cdef:
    bint sb_win
    int win_amount

  def __init__(self, bint sb_win, int win_amount):
    self.sb_win = sb_win
    self.win_amount = win_amount
    super(FoldNode, self).__init__(num_round=-1)

  cdef void transit(self, float p_sb, float p_bb, float* util_sb, float* util_bb,
                    int* bucket_seq_sb, int* bucket_seq_bb):
    if self.sb_win:
      util_sb[0] = self.win_amount
      util_bb[0] = -self.win_amount
    else:
      util_sb[0] = -self.win_amount
      util_bb[0] = self.win_amount      

  
cdef class ShowdownNode(Node):
  cdef int pot_size

  def __init__(self, int pot_size):
    self.pot_size = pot_size
    super(ShowdownNode, self).__init__(num_round=-1)

  cdef void transit(self, float p_sb, float p_bb, float* util_sb, float* util_bb,
                    int* bucket_seq_sb, int* bucket_seq_bb):
    if bucket_seq_sb[4] > bucket_seq_bb[4]:
      util_sb[0] = self.pot_size/2
      util_bb[0] = -self.pot_size/2
    elif bucket_seq_sb[4] < bucket_seq_bb[4]:
      util_sb[0] = -self.pot_size/2
      util_bb[0] = self.pot_size/2
    else:
      util_sb[0] = 0
      util_bb[0] = 0
