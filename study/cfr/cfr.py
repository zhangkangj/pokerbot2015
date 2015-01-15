# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 16:19:06 2015

@author: zhk
"""

class Node(object):
  def __init__(self, active_player, num_round, 
               bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack1, stack2, amount_sb, amount_bb):
    self.active_player = active_player # SB or BB
    self.num_round = num_round
    self.bucket_sequence_sb = None
    self.bucket_sequence_bb = None
    self.pot_size = pot_size # pot size at the begining of the round
    self.stack_sb = stack_sb
    self.stack_bb = stack_bb
    self.bet_amount1 = amount_sb
    self.bet_amount2 = amount_bb
    self.child_nodes = []

  def transit(self):
    pass
  
class RoundNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    super(RoundNode, self).__init__(num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    if self.num_round == 0:
      self.child_nodes.append(RaiseNode('SB', num_round, 
                                        bucket_sequence_sb, bucket_sequence_bb,
                                        0, amount_sb-1, amount_bb-2, 1, 2))
    else:
      self.child_nodes.append(RaiseNode('SB', num_round, 
                                        bucket_sequence_sb, bucket_sequence_bb,
                                        pot_size, amount_sb, amount_bb, 0, 0))

class RaiseNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    super(RaiseNode, self).__init__(num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    

class CheckNode(Node):
  def __init__(self):
    super(CheckNode, self).__init__()

class CallNode(Node):
  def __init__(self):
    super(CallNode, self).__init__()

class FoldNode(Node):
  def __init__(self):
    super(FoldNode, self).__init__()
