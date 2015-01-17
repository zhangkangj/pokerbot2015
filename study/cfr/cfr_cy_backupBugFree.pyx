# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 16:19:06 2015

@author: zhk
"""

import numpy as np
cimport numpy as np

cdef int MAX_BET_NUM = 3

cdef class Node(object):
  cpdef bucket_sequence_sb
  cpdef bucket_sequence_bb
  cpdef child_nodes    
  
  cdef:
    float* utility_sb_ptr
    float* utility_bb_ptr
    int active_player
    int num_round
    int pot_size
    int stack_sb, stack_bb
    int amount_sb, amount_bb
    int num_child
    int num_card_bucket

  def __init__(self, active_player, num_round, 
               bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    #assert pot_size + stack_sb + stack_bb + amount_sb + amount_bb == 600, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    assert pot_size >= 0 and stack_sb >= 0 and stack_bb >= 0 and amount_sb >= 0 and amount_bb >= 0, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    self.active_player = active_player # SB = 1, BB = 2, dealer = 0
    self.num_round = num_round
    self.bucket_sequence_sb = bucket_sequence_sb
    self.bucket_sequence_bb = bucket_sequence_bb
    self.pot_size = pot_size # pot size at the begining of the round
    self.stack_sb = stack_sb
    self.stack_bb = stack_bb
    self.amount_sb = amount_sb
    self.amount_bb = amount_bb
    self.child_nodes = []
    if num_round == 0:
      self.num_card_bucket = 169
    elif self.num_round == 1:
      self.num_card_bucket = 10
    elif self.num_round == 2:
      self.num_card_bucket = 10
    elif self.num_round == 3:
      self.num_card_bucket = 10
    else:
      self.num_card_bucket = 0

  cdef get_next_player(self):
    cdef int next_player
    if self.active_player == 0:
      if self.num_round == 0:
        next_player = 1
      else:
        next_player = 2
    else:
      next_player = self.active_player % 2 + 1
    return next_player

  def spawn_round_node(self, pot_size, stack_sb, stack_bb, final_amount_sb, final_amount_bb):
    node = RoundNode(self.num_round+1, self.bucket_sequence_sb, self.bucket_sequence_bb,
                     pot_size, stack_sb, stack_bb, final_amount_sb, final_amount_bb)
    self.child_nodes.append(node)

  def spawn_raise_node(self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb,
                       min_bet, num_bet, raise_amount):
    active_player = self.get_next_player()
    assert active_player != 0
    node = RaiseNode(active_player, self.num_round, self.bucket_sequence_sb, self.bucket_sequence_bb,
                     pot_size, stack_sb, stack_bb, amount_sb, amount_bb,
                     min_bet, num_bet, raise_amount)              
    self.child_nodes.append(node)

  def spawn_check_node(self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    active_player = self.get_next_player()
    node = CheckNode(active_player, self.num_round, self.bucket_sequence_sb, self.bucket_sequence_bb,
                     pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    self.child_nodes.append(node)

  def spawn_fold_node(self, pot_size, stack_sb, stack_bb):
    assert self.active_player != 0
    active_player = self.get_next_player() # active is the winner
    node = FoldNode(active_player, pot_size, stack_sb, stack_bb)
    self.child_nodes.append(node)

  def spawn_showdown_node(self, pot_size, stack_sb, stack_bb):
    node = ShowdownNode(self.bucket_sequence_sb, self.bucket_sequence_bb,
                         pot_size, stack_sb, stack_bb)
    self.child_nodes.append(node)

  def traverse(self):
    count = 1 
    if len(self.child_nodes) == 0:
      return count
    else:
      for node in self.child_nodes:
        count += node.traverse()
      return count

  def traverse_game_round(self, game_round):
    count = 1 if self.num_round == game_round and self.active_player > 0 else 0
    if len(self.child_nodes) == 0:
      return count
    else:
      for node in self.child_nodes:
        count += node.traverse_game_round(game_round)
      return count

  def traverse_pot_greater_than(self, pot_threshold):
    count = 1 if (self.active_player > 0 and (self.pot_size+self.amount_sb+self.amount_bb) > pot_threshold) else 0
    if len(self.child_nodes) == 0:
      return count
    else:
      for node in self.child_nodes:
        count += node.traverse_pot_greater_than(pot_threshold)
      return count

  def traverse_node_type(self, game_round, node_type):
    #print self.amount_bb, self.amount_sb
    if node_type == 'Raise':
      if self.amount_bb == 2 and self.amount_sb == 2 and self.active_player == 2 and self.num_round == 0:
        is_type = False
      else:
        is_type = self.amount_bb > 0 or self.amount_sb > 0     
    elif node_type == 'Check':
      if self.amount_bb == 2 and self.amount_sb == 2 and self.active_player == 2 and self.num_round == 0:
        is_type = True
      else:
        is_type = self.amount_bb == 0 and self.amount_sb == 0

        
    
    count = 1 if (self.active_player > 0 and self.num_round == game_round and is_type) else 0
    if len(self.child_nodes) == 0:
      return count
    else:
      for node in self.child_nodes:
        count += node.traverse_node_type(game_round, node_type)
      return count      
  def traverse_graph(self, previous_act):
    if self.active_player == 0:
      move = ':DEALCARD:' + str(self.num_round)
    elif (self.amount_bb > 0 or self.amount_sb > 0):
      move = ':Raise:' + str(max(self.amount_sb, self.amount_bb))
    elif self.amount_bb == 0 and self.amount_sb == 0:
      move = ':Check'
      
    
    move = str(3 - self.active_player) + move
    prev1 = previous_act + [move]
    if self.num_round > -1 and self.active_player > 0:
      print ' '.join(prev1),'\n'
    if len(self.child_nodes) == 0:
      return prev1
    else:
      for node in self.child_nodes:
        node.traverse_graph(prev1)
      return prev1
      
  def transit(self, p_sb, p_bb):
    pass
    #return u_sb, u_bb


cdef class RoundNode(Node):
  cdef:
    int preflop_amount_sb, preflop_amount_bb
    int flop_amount_sb, flop_amount_bb
    int turn_amount_sb, turn_amount_bb
    int river_amount_sb, river_amount_bb

  def __init__(self, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb=0, amount_bb=0):
    super(RoundNode, self).__init__(0, num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    self.num_child = 1
    if self.num_round == 0:
      assert pot_size == 0
      assert stack_sb == stack_bb
      self.amount_sb, self.amount_bb = 1, 2
      self.spawn_raise_node(pot_size, stack_sb-1, stack_bb-2, self.amount_sb, self.amount_bb, min_bet=2, num_bet=0, raise_amount=2)
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
      self.spawn_check_node(pot_size, stack_sb, stack_bb, amount_sb=0, amount_bb=0)
#  def transit(self, p_sb, p_bb):
#    self.child_nodes[0].transit(p_sb, p_bb)
#    self.utility_bb[self.bucket_sequence_bb[self.num_round]] = self.child_nodes[0].utility_bb[self.bucket_sequence_bb[self.num_round]]
#    self.utility_sb[self.bucket_sequence_sb[self.num_round]] = self.child_nodes[0].utility_sb[self.bucket_sequence_sb[self.num_round]]
cdef class RaiseNode(Node):
  cpdef regret
  cdef float* regret_ptr

  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb, min_bet, num_bet, raise_amount):
    super(RaiseNode, self).__init__(active_player, num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    print self.active_player, self.amount_sb, self.amount_bb, self.pot_size,self.num_round
    # player folds
    self.spawn_fold_node(pot_size+amount_sb+amount_bb, stack_sb, stack_bb)
    # player calls
    call_amount = abs(amount_bb - amount_sb)
    stack, sb_delta, bb_delta = (stack_sb, call_amount, 0) if active_player == 1 else (stack_bb, 0, call_amount)
    if stack <= call_amount:
      self.spawn_showdown_node(pot_size+amount_sb+amount_bb+call_amount, stack_sb-sb_delta, stack_bb-bb_delta)
    else:
      if num_round < 3:
        # SB calls BB after post blinds
        if num_round == 0 and active_player == 1 and amount_sb == 1 and amount_bb == 2:
          self.spawn_check_node(pot_size, stack_sb-1, stack_bb, amount_sb=2, amount_bb=2)
        else:
        # player calls before river
          self.spawn_round_node(pot_size+amount_sb+amount_bb+call_amount, 
                                stack_sb-sb_delta, stack_bb-bb_delta,
                                final_amount_sb=0, final_amount_bb=0) # TODO fix final amount
      else:
        # player calls at river
        self.spawn_showdown_node(pot_size+amount_sb+amount_bb+call_amount, stack_sb-sb_delta, stack_bb-bb_delta)
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
          sb_delta_, bb_delta_ = (raise_amount+sb_delta, 0) if active_player == 1 else (0, raise_amount+bb_delta)
          assert amount_sb+sb_delta_!= amount_bb+bb_delta_
          self.spawn_raise_node(pot_size, stack_sb-sb_delta_, stack_bb-bb_delta_,
                                amount_sb+sb_delta_, amount_bb+bb_delta_, raise_amount, num_bet+1, raise_amount)
    self.num_child = len(self.child_nodes)

#  cdef void transit(self, p_sb, p_bb):
#    cdef float* act_prob
#    cdef int node_bucket
#    act_prob = (float *)malloc(5 * sizeof(float))  
#    #update action probablity from regret    
#    #traverse tree to compute utilities of child nodes
#    if self.active_player == 'SB':
#      node_bucket = self.bucket_sequence_sb[self.num_round]
#      compute_prob(act_prob, node_bucket)
#      for i in range(0, self.num_child):
#        self.child_nodes[i].translate(p_sb * act_prob[i], p_bb)
#    #compute utility from utilities of child nodes     
#      for i in range(0, self.num_child):
#        self.utility_sb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_sb[node_bucket]
#        self.utility_bb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_bb[node_bucket] 
#    #compute new regrets
#      for i in range(0, self.num_child):
#        self.regret[node_bucket * 5 + i] *= T * 1. / (T + 1)
#        self.regret[node_bucket * 5 + i] += p_bb * (self.child_nodes[i].utility_sb[node_bucket] - self.utility_sb[node_bucket]) / (T + 1)
#    else:
#      node_bucket = self.bucket_sequence_sb[self.num_round]
#      compute_prob(act_prob, node_bucket)
#      for i in range(0, self.num_child):
#        self.child_nodes[i].translate(p_sb, p_bb * act_prob[i])
#    #compute utility from utilities of child nodes     
#      for i in range(0, self.num_child):
#        self.utility_sb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_sb[node_bucket]
#        self.utility_bb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_bb[node_bucket]
#    #compute new regrets
#      for i in range(0, self.num_child):
#        self.regret[node_bucket * 5 + i] *= T * 1. / (T + 1)
#        self.regret[node_bucket * 5 + i] += p_sb * (self.child_nodes[i].utility_bb[node_bucket] - self.utility_bb[node_bucket]) / (T + 1)
#        
#            
#        
#  cdef void compute_prob(float* XXX, int node_bucket):
#    cdef float sum_regret_plus = 0
#    for i in range(0, self.num_child):
#      self.regret[node_bucket + i] = max(self.regret[node_bucket + i], 0)
#      sum_regret_plus += self.regret[node_bucket + i]
#    if sum_regret_plus > 0:
#      for i in range(0, self.num_child):
#        XXX[i] /= sum_regret_plus
#    else:
#      tmp = 1./self.num_child
#      for i in range(0, self.num_child):
#        XXX[i] = tmp
#    return

cdef class CheckNode(Node):
  cpdef regret
  cdef float* regret_ptr

  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    super(CheckNode, self).__init__(active_player,num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    print self.active_player, self.amount_sb, self.amount_bb, self.pot_size,self.num_round

    # player checks
    if (self.num_round==0 and active_player==1) or (self.num_round>0 and active_player==2):
      self.spawn_check_node(pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    else:
      if self.num_round == 3:
        assert amount_sb==amount_bb==0
        self.spawn_showdown_node(pot_size, stack_sb, stack_bb)
      else:
        self.spawn_round_node(pot_size+amount_sb+amount_bb, stack_sb, stack_bb,
                              final_amount_sb=0, final_amount_bb=0) # TODO fix final amount
    # player bets
    raise_limit = stack_sb if active_player == 1 else stack_bb
    desired_amounts = [2 , (pot_size+amount_sb+amount_bb)/2, pot_size+amount_sb+amount_bb]
    #desired_amounts = [(pot_size+amount_sb+amount_bb)/2, pot_size+amount_sb+amount_bb]
    if raise_limit < pot_size + amount_sb + amount_bb:
      raise_amounts = set([amount for amount in desired_amounts if amount < raise_limit] + [raise_limit])
    else:
      raise_amounts = set(desired_amounts)
    for raise_amount in raise_amounts:
      sb_delta, bb_delta = (raise_amount, 0) if active_player == 1 else (0, raise_amount)
      self.spawn_raise_node(pot_size, stack_sb-sb_delta, stack_bb-bb_delta,
                            amount_sb+sb_delta, amount_bb+bb_delta, raise_amount, num_bet=1, raise_amount=raise_amount)
    self.num_child = len(self.child_nodes)


#  cdef void transit(self, p_sb, p_bb):
#    cdef float* act_prob
#    cdef int node_bucket
#    act_prob = (float *)malloc(5 * sizeof(float))  
#    #update action probablity from regret    
#    #traverse tree to compute utilities of child nodes
#    if self.active_player == 'SB':
#      node_bucket = self.bucket_sequence_sb[self.num_round]
#      compute_prob(act_prob, node_bucket)
#      for i in range(0, self.num_child):
#        self.child_nodes[i].translate(p_sb * act_prob[i], p_bb)
#    #compute utility from utilities of child nodes     
#      for i in range(0, self.num_child):
#        self.utility_sb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_sb[node_bucket]
#        self.utility_bb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_bb[node_bucket] 
#    #compute new regrets
#      for i in range(0, self.num_child):
#        self.regret[node_bucket * 5 + i] *= T * 1. / (T + 1)
#        self.regret[node_bucket * 5 + i] += p_bb * (self.child_nodes[i].utility_sb[node_bucket] - self.utility_sb[node_bucket]) / (T + 1)
#    else:
#      node_bucket = self.bucket_sequence_sb[self.num_round]
#      compute_prob(act_prob, node_bucket)
#      for i in range(0, self.num_child):
#        self.child_nodes[i].translate(p_sb, p_bb * act_prob[i])
#    #compute utility from utilities of child nodes     
#      for i in range(0, self.num_child):
#        self.utility_sb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_sb[node_bucket]
#        self.utility_bb[node_bucket] += act_prb[i] * self.child_nodes[i].utility_bb[node_bucket]
#    #compute new regrets
#      for i in range(0, self.num_child):
#        self.regret[node_bucket * 5 + i] *= T * 1. / (T + 1)
#        self.regret[node_bucket * 5 + i] += p_sb * (self.child_nodes[i].utility_bb[node_bucket] - self.utility_bb[node_bucket]) / (T + 1)
#        
#            
#        
#  cdef void compute_prob(float* XXX, int node_bucket):
#    cdef float sum_regret_plus = 0
#    for i in range(0, self.num_child):
#      self.regret[node_bucket + i] = max(self.regret[node_bucket + i], 0)
#      sum_regret_plus += self.regret[node_bucket + i]
#    if sum_regret_plus > 0:
#      for i in range(0, self.num_child):
#        XXX[i] /= sum_regret_plus
#    else:
#      tmp = 1./self.num_child
#      for i in range(0, self.num_child):
#        XXX[i] = tmp
#    return

cdef class FoldNode(Node):
  cdef int winner
  def __init__(self, active_player, pot_size, stack_sb, stack_bb):
    super(FoldNode, self).__init__(0, -1, None, None, 
                                   pot_size, stack_sb, stack_bb, 0, 0)
    self.winner = self.active_player
    self.num_child = 0


cdef class ShowdownNode(Node):
  def __init__(self, bucket_sequence_sb, bucket_sequence_bb, pot_size, stack_sb, stack_bb):
    super(ShowdownNode, self).__init__(0, -1, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, 0, 0)
    self.num_child = 0
