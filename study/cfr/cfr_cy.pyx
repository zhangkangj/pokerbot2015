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
    int active_player
    int num_round
    int pot_size
    int stack_sb, stack_bb
    int amount_sb, amount_bb
    int num_child
    
  def __init__(self, active_player, num_round, 
               bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    assert pot_size + stack_sb + stack_bb + amount_sb + amount_bb == 600, (self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
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

  def spawn_round_node(self, pot_size, stack_sb, stack_bb):
    node = RoundNode(self.num_round+1, self.bucket_sequence_sb, self.bucket_sequence_bb,
                 pot_size, stack_sb, stack_bb)
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

  def transit(self, p_sb, p_bb):
    pass
    #return u_sb, u_bb

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

cdef class RoundNode(Node):
  def __init__(self, num_round, bucket_sequence_sb, bucket_sequence_bb, pot_size, stack_sb, stack_bb):
    super(RoundNode, self).__init__(0, num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb=0, amount_bb=0)
    if self.num_round == 0:
      assert pot_size == 0
      assert stack_sb == stack_bb
      self.amount_sb, self.amount_bb = 1, 2
      self.spawn_raise_node(pot_size, stack_sb-1, stack_bb-2, self.amount_sb, self.amount_bb, min_bet=2, num_bet=0, raise_amount=2)
    else:
      self.spawn_check_node(pot_size, stack_sb, stack_bb, self.amount_sb, self.amount_bb)


cdef class RaiseNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb, min_bet, num_bet, raise_amount):
    super(RaiseNode, self).__init__(active_player, num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
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
          self.spawn_round_node(pot_size+amount_sb+amount_bb+call_amount, stack_sb-sb_delta, stack_bb-bb_delta)
      else:
        # player calls at river
        self.spawn_showdown_node(pot_size+amount_sb+amount_bb+call_amount, stack_sb-sb_delta, stack_bb-bb_delta)
      # player raises
      if num_bet < MAX_BET_NUM:
        raise_limit = stack - call_amount
        # desired_amounts = [2, pot_size+amount_sb+amount_bb+call_amount]
        desired_amounts = [min_bet , (pot_size+amount_sb+amount_bb+call_amount)/2, pot_size+amount_sb+amount_bb+call_amount]
        if raise_limit < pot_size + amount_sb + amount_bb + call_amount:
          raise_amounts = set([amount for amount in desired_amounts if amount < raise_limit] + [raise_limit])
        else:
          raise_amounts = set(desired_amounts)
        for raise_amount in raise_amounts:
          sb_delta_, bb_delta_ = (raise_amount+sb_delta, 0) if active_player == 1 else (0, raise_amount+bb_delta)
          self.spawn_raise_node(pot_size, stack_sb-sb_delta_, stack_bb-bb_delta_,
                                amount_sb+sb_delta_, amount_bb+bb_delta_, raise_amount, num_bet+1, raise_amount)


cdef class CheckNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    super(CheckNode, self).__init__(active_player,num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    # player checks
    if (self.num_round==0 and active_player==1) or (self.num_round>0 and active_player==2):
      self.spawn_check_node(pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    else:
      if self.num_round == 3:
        assert amount_sb==amount_bb==0
        self.spawn_showdown_node(pot_size, stack_sb, stack_bb)
      else:
        self.spawn_round_node(pot_size+amount_sb+amount_bb, stack_sb, stack_bb)
    # player bets
    raise_limit = stack_sb if active_player == 1 else stack_bb
    desired_amounts = [2 , (pot_size+amount_sb+amount_bb)/2, pot_size+amount_sb+amount_bb]
    # desired_amounts = [2, pot_size+amount_sb+amount_bb]
    if raise_limit < pot_size + amount_sb + amount_bb:
      raise_amounts = set([amount for amount in desired_amounts if amount < raise_limit] + [raise_limit])
    else:
      raise_amounts = set(desired_amounts)
    for raise_amount in raise_amounts:
      sb_delta, bb_delta = (raise_amount, 0) if active_player == 1 else (0, raise_amount)
      self.spawn_raise_node(pot_size, stack_sb-sb_delta, stack_bb-bb_delta,
                            amount_sb+sb_delta, amount_bb+bb_delta, raise_amount, num_bet=1, raise_amount=raise_amount)


cdef class FoldNode(Node):
  cdef int winner
  def __init__(self, active_player, pot_size, stack_sb, stack_bb):
    super(FoldNode, self).__init__(0, -1, None, None, 
                                   pot_size, stack_sb, stack_bb, 0, 0)
    self.winner = self.active_player


cdef class ShowdownNode(Node):
  def __init__(self, bucket_sequence_sb, bucket_sequence_bb, pot_size, stack_sb, stack_bb):
    super(ShowdownNode, self).__init__(0, -1, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, 0, 0)
