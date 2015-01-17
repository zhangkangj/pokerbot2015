# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 16:19:06 2015

@author: zhk
"""

import numpy as np

MAX_BET_NUM = 3

class Node(object):
  count = 0
  round_count = 0
  raise_count = 0
  check_count = 0
  fold_count = 0
  showdown_count = 0
  def __init__(self, active_player, num_round, 
               bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    Node.count += 1
    self.active_player = active_player # SB or BB
    self.num_round = num_round
    self.bucket_sequence_sb = None
    self.bucket_sequence_bb = None
    self.pot_size = pot_size # pot size at the begining of the round
    self.stack_sb = stack_sb
    self.stack_bb = stack_bb
    self.amount_sb = amount_sb
    self.amount_bb = amount_bb
    self.child_nodes = []

  def get_next_player(self):
    if self.active_player is None:
      if self.num_round == 0:
        next_player = "SB"
      else:
        next_player = "BB" 
    elif self.active_player == 'BB':
      next_player = 'SB'
    elif self.active_player == 'SB':
      next_player = 'BB'
    else:
      assert 1==0, ('invalid player', self.active_player)
    return next_player

  def spawn_round_node(self, pot_size, stack_sb, stack_bb):
    node = RoundNode(self.num_round+1, self.bucket_sequence_sb, self.bucket_sequence_bb,
                 pot_size, stack_sb, stack_bb)
    self.child_nodes.append(node)

  def spawn_raise_node(self, pot_size, stack_sb, stack_bb, amount_sb, amount_bb,
                       min_bet, num_bet, raise_amount):
    active_player = self.get_next_player()
    assert active_player is not None
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
    assert self.active_player is not None
    active_player = self.get_next_player() # active is the winner
    node = FoldNode(active_player, pot_size, stack_sb, stack_bb)
    self.child_nodes.append(node)

  def spawn_showdown_node(self, pot_size, stack_sb, stack_bb):
    node = ShowdownNode(self.bucket_sequence_sb, self.bucket_sequence_bb,
                         pot_size, stack_sb, stack_bb)
    self.child_nodes.append(node)

  def transit(self, p_sb, p_bb):
    return u_sb, u_bb


class RoundNode(Node):
  def __init__(self, num_round, bucket_sequence_sb, bucket_sequence_bb, pot_size, stack_sb, stack_bb):
    super(RoundNode, self).__init__(None, num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb=0, amount_bb=0)
    Node.round_count += 1
#    print 'round', Node.round_count
    if self.num_round == 0:
      assert pot_size == 0
      assert stack_sb == stack_bb
      Node.count = 0
      self.amount_sb, self.amount_bb = 1, 2
      self.spawn_raise_node(pot_size, stack_sb -1 , stack_bb-2, self.amount_sb, self.amount_bb, min_bet=2, num_bet=0, raise_amount=2)
    else:
      self.spawn_check_node(pot_size, stack_sb, stack_bb, self.amount_sb, self.amount_bb)


class RaiseNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb, min_bet, num_bet, raise_amount):
    super(RaiseNode, self).__init__(active_player, num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    Node.raise_count += 1
#    print 'raise', Node.raise_count
    # player folds
    self.spawn_fold_node(pot_size+amount_sb+amount_bb, stack_sb, stack_bb)
    # player calls
    call_amount = abs(amount_bb - amount_sb)
    stack, sb_delta, bb_delta = (stack_sb, call_amount, 0) if active_player == 'SB' else (stack_bb, 0, call_amount)
    if stack <= call_amount:
      self.spawn_showdown_node(pot_size+amount_sb+amount_bb+call_amount, stack_sb-sb_delta, stack_bb-bb_delta)
    else:
      if num_round < 3:
        # SB calls BB after post blinds
        if num_round == 0 and active_player == 'SB' and amount_sb == 1 and amount_bb == 2:
          self.spawn_check_node(pot_size, stack_sb-1, stack_bb, amount_sb=2, amount_bb=2)
        else:
        # player calls before river
          self.spawn_round_node(pot_size+amount_sb+amount_bb+call_amount, stack_sb-sb_delta, stack_bb-bb_delta)
      else:
        # player calls at river
        self.spawn_showdown_node(pot_size+amount_sb+amount_bb+call_amount, stack_sb-sb_delta, stack_bb-bb_delta)
      # player raises
      if num_bet < MAX_BET_NUM:
 #       print min_bet, pot_size, amount_bb,amount_sb
        raise_limit = stack - call_amount
        # desired_amounts = [2, pot_size+amount_sb+amount_bb+call_amount]
        desired_amounts = [min_bet , (pot_size+amount_sb+amount_bb+call_amount)/2, pot_size+amount_sb+amount_bb+call_amount]
        if raise_limit < pot_size+amount_sb+amount_bb+call_amount:
          raise_amounts = set([amount for amount in desired_amounts if amount < raise_limit] + [raise_limit])
        else:
          raise_amounts = set(desired_amounts)
  #      print raise_amounts, desired_amounts, raise_limit
        if len(desired_amounts) < 3:
          print desired_amounts
        for raise_amount in raise_amounts:
          sb_delta, bb_delta = (raise_amount+sb_delta, 0) if active_player == 'SB' else (0, raise_amount+bb_delta)
          self.spawn_raise_node(pot_size, stack_sb-sb_delta, stack_bb-bb_delta,
                                amount_sb+sb_delta, amount_bb+bb_delta, raise_amount, num_bet+1, raise_amount)


class CheckNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    super(CheckNode, self).__init__(active_player,num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    Node.check_count += 1
 #   print 'check', Node.check_count
    # player checks
    if (self.num_round==0 and active_player=='SB') or (self.num_round>0 and active_player=='BB'):
      self.spawn_check_node(pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    else:
      if self.num_round == 3:
        self.spawn_showdown_node(pot_size, stack_sb, stack_bb)
      else:
        self.spawn_round_node(pot_size + amount_sb + amount_bb, stack_sb, stack_bb)
    # player bets
    raise_limit = stack_sb if active_player == 'SB' else stack_bb
    desired_amounts = [2 , (pot_size+amount_sb+amount_bb)/2, pot_size+amount_sb+amount_bb]
 #   print desired_amounts, raise_limit, amount_sb, amount_bb
    # desired_amounts = [2, pot_size+amount_sb+amount_bb]
    if raise_limit < pot_size+amount_sb+amount_bb:
      raise_amounts = set([amount for amount in desired_amounts if amount < raise_limit] + [raise_limit])
    else:
      raise_amounts = set(desired_amounts)
    for raise_amount in raise_amounts:
      sb_delta, bb_delta = (raise_amount, 0) if active_player == 'SB' else (0, raise_amount)
      self.spawn_raise_node(pot_size, stack_sb-sb_delta, stack_bb-bb_delta,
                            amount_sb+sb_delta, amount_bb+bb_delta, raise_amount, num_bet=1, raise_amount=raise_amount)


class FoldNode(Node):
  def __init__(self, active_player, pot_size, stack_sb, stack_bb):
    super(FoldNode, self).__init__(None, None, None, None, 
                                   pot_size, stack_sb, stack_bb, 0, 0)
    self.winner = self.active_player
    Node.fold_count += 1
 #   print 'fold', Node.fold_count


class ShowdownNode(Node):
  def __init__(self, bucket_sequence_sb, bucket_sequence_bb, pot_size, stack_sb, stack_bb):
    super(ShowdownNode, self).__init__(None, None, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, 0, 0)
    Node.showdown_count += 1
#    print 'showdown', Node.showdown_count


if __name__ == "__main__":
  root = RoundNode(0, None, None, 0, 300, 300)
  print Node.count, Node.round_count, Node.raise_count, Node.check_count, Node.fold_count, Node.showdown_count
