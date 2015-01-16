# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 16:19:06 2015

@author: zhk
"""


import numpy as np
MAX_BET_NUM = 4
class Node(object):
  def __init__(self, active_player, num_round, 
               bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
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
    super(RoundNode, self).__init__( active_player, num_round , active_player, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    
    if self.num_round == 0:
      self.child_nodes.append(RaiseNode('SB', num_round, 
                                        bucket_sequence_sb, bucket_sequence_bb,
                                        0, stack_sb-1, stack_bb-2, 1, 2, 2, 2, 0))
    else:
      self.child_nodes.append(CheckNode('SB', num_round, 
                                        bucket_sequence_sb, bucket_sequence_bb,
                                        pot_size, stack_sb, stack_bb, 0, 0, 2))

class RaiseNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb, min_bet, num_bet, raise_amount):
    super(RaiseNode, self).__init__( active_player,num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    #if the player folds
    self.child_nodes.append(FoldNode(active_player, num_round, 
                                     bucket_sequence_sb, bucket_sequence_bb,
                                     pot_size,stack_sb,stack_bb))
    sb_is_active = (active_player == 'SB')
    if sb_is_active:
      call_amount = amount_bb - amount_sb
      stack = stack_sb
      opponent = 'BB'
    else:
      call_amount = amount_sb - amount_bb
      stack = stack_bb
      opponent = 'SB'
    #player calls
    #stack too small, can only call
    if stack <= call_amount:
      self.child_nodes.append(ShowDownNode(None, num_round, bucket_sequence_sb, bucket_sequence_bb,
                                           pot_size + stack, stack_sb - int(sb_is_active) * stack, stack_bb - int(not(sb_is_active)) * stack))      
    else:
      if num_round < 3:
        #SB calls BB after post blinds
        if num_round == 0 and sb_is_active and pot_size == 3:
          self.child_nodes.append(CheckNode(active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
                                            pot_size + 1, stack_sb - int(sb_is_active) * call_amount, 
                                            stack_bb - int(not(sb_is_active)) * call_amount), 2 , 2)
        else:
          self.child_nodes.append(RoundNode(None, num_round + 1, bucket_sequence_sb, bucket_sequence_bb, pot_size + call_amount, 
                                            stack_sb - int(sb_is_active) * call_amount, stack_bb - int(not(sb_is_active)) * call_amount, 
                                            amount_sb + int(sb_is_active) * call_amount, amount_bb + int(not(sb_is_active)) * call_amount))
      else: 
        self.child_nodes.append(ShowDownNode(None, num_round, bucket_sequence_sb, bucket_sequence_bb, pot_size + call_amount, 
                                             stack_sb - int(sb_is_active) * call_amount, stack_bb - int(not(sb_is_active)) * call_amount))   
      #player raises
      if num_bet == MAX_BET_NUM:
        pass
      else:
        raise_limit = stack - call_amount
        desired_amount = [min_bet , pot_size/2, pot_size]
        if raise_limit <= pot_size:
          desired_amount = [amount for amount in desired_amount if amount < raise_limit] + [raise_limit] 
        else:
          pass
        for x in desired_amount:
          self.child_nodes.append(RaiseNode(opponent, num_round, bucket_sequence_sb, bucket_sequence_bb, pot_size + (x + call_amount),
                                            stack_sb - int(sb_is_active) * (x + call_amount), stack_bb - int(not(sb_is_active)) * (x + call_amount),
                                            amount_sb + int(sb_is_active) * (x + call_amount), amount_bb + int(not(sb_is_active)) * (x + call_amount),                    
                                            x, num_bet + 1, x)) 

class CheckNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb, amount_sb, amount_bb):
    super(RaiseNode, self).__init__(active_player,num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, amount_sb, amount_bb)
    #if the player folds
    self.child_nodes.append(FoldNode(active_player, num_round, 
                                     bucket_sequence_sb, bucket_sequence_bb,
                                     pot_size,stack_sb,stack_bb))
    sb_is_active = (active_player == 'SB')
    if sb_is_active:
      stack = stack_sb
      opponent = 'BB'
    else:
      stack = stack_bb
      opponent = 'SB'
    #player checks
    if sb_is_active:
      self.child_nodes.append(CheckNode(opponent, num_round, bucket_sequence_sb, bucket_sequence_bb,
                                        pot_size, stack_sb, stack_bb, amount_sb, amount_bb))
    else:
      if num_round == 3:
        self.child_nodes.append(ShowDownNode(None, num_round, bucket_sequence_sb, bucket_sequence_bb,
                                             pot_size, stack_sb, stack_bb))
      else:
        self.child_nodes.append(RoundNode(None, num_round + 1, bucket_sequence_sb, bucket_sequence_bb,
                                          pot_size, stack_sb, stack_bb))
    #player bets
    raise_limit = stack
    desired_amount = [2 , pot_size/2, pot_size]
    if raise_limit <= pot_size:
      desired_amount = [amount for amount in desired_amount if amount < raise_limit] + [raise_limit] 
    else:
      pass
    for x in desired_amount:
      self.child_nodes.append(RaiseNode(opponent, num_round, bucket_sequence_sb, bucket_sequence_bb, pot_size + x, 
                                        stack_sb - int(sb_is_active) * x, stack_bb - int(not(sb_is_active)) * x,
                                        amount_sb + int(sb_is_active) * x, amount_bb + int(not(sb_is_active)) * x,
                                        x, 1, x))     

  

class FoldNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb):
    super(FoldNode, self).__init__(active_player,num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, 0, 0)
class ShowDownNode(Node):
  def __init__(self, active_player, num_round, bucket_sequence_sb, bucket_sequence_bb,
               pot_size, stack_sb, stack_bb):
    super(ShowDownNode, self).__init__(active_player, num_round, bucket_sequence_sb, bucket_sequence_bb, 
                                    pot_size, stack_sb, stack_bb, 0, 0)

