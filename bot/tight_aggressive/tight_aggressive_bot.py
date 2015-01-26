
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot
from lib.evaluator import evaluator
from lib import util
import numpy as np
import scipy.stats as sp

class TightAggressiveBot(base_bot.BaseBot):

  def __init__(self,player):
    self.flop_buckets = np.load('../../data/evaluator/flop_bucket.npy')
    self.turn_buckets = np.load('../../data/evaluator/turn_bucket.npy') 
    self.prob_arr = np.load('../../data/evaluator/preflop_prob.npy')
    self.player = player
    
  def action(self):
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
    return super(TightAggressiveBot, self).action(can_raise, can_bet, can_call)

  def preflop_idx(self,cards):
    c = util.c2n(cards)
    c1 = c[0]
    c2 = c[1]
    r1 = c1 / 4
    r2 = c2 / 4
    if r1 > r2:
      result = r1*(r1-1)/2 + r2
    elif r1 < r2:
      result = r2*(r2-1)/2 + r1
    else:
      result = 78 + r1
    if (c1&0b11) == (c2&0b11):
      result += 91
    return result
    
  def num_of_raise(self,last_actions):
    num = len([action for action in last_actions if 'RAISE' in action or 'BET' in action])
    return num
    
  def cal_equity(self, bucket):
    equity = 0
    var = 0
    if self.player.num_board_card == 3:
      if bucket <=11:
        equity = 0.1 + bucket * 0.075 + 0.075/2
        var = 0.05
      elif bucket <=24:
        equity = 0.15 + (bucket - 12) * 0.05 + 0.05/2
        var = 0.1
      elif bucket <=29:
        equity = 0.2 + (bucket - 25)*0.1 + 0.05
        var = 0.13
      elif bucket == 30:
        equity = 0.25
        var = 0.2
      else:
        equity = 0.45
        var = 0.2
    elif self.player.num_board_card == 4:
      if bucket <= 18:
        equity = 0.05 + bucket * 0.05 + 0.05/2
        var = 0.025
      elif bucket <=26:
        equity = 0.1 + (bucket - 19) * 0.075 + 0.075/2
        var = 0.04
      elif bucket <=30:
        equity = 0.1 + (bucket - 27)*0.1 + 0.05
        var = 0.055
      else:
        equity = 0.25
        var = 0.1
    return equity
    
  
  
  def preflop(self, can_raise, can_bet, can_call):
    tight_level = 2.5  # the larger, the tighter, affecting folding probability    
    call_limit = 10  # max call size, otherwise fold
    decay_factor = 0.6 # probability of raising decay, affecting raising probability
    num_raise = self.num_of_raise(self.player.last_actions_preflop)
    decay = decay_factor ** num_raise
    print 'decay factor is ', decay
    hole_card_idx = self.preflop_idx(self.player.hole_cards)
    prob = self.prob_arr[hole_card_idx]
    
    prob[2] = prob[2]*decay
    prob[3] = prob[3]*decay
    prob[1] = 1 - prob[0] - prob[2] - prob[3]    
    
    prob_modified = np.zeros(4)
    prob_modified[0] = min(1, prob[0]*tight_level)
    for i in range(1,4):
      prob_modified[i] = prob[i]*(1-prob_modified[0])/(1-prob[0])
      
    print 'Check/Fold prob:',prob_modified[0],', Call Prob:', prob_modified[1], 'Half Raise Prob:', prob_modified[2], ', Raise Prob:', prob_modified[3]
    print 'Sum check:', sum(prob_modified)    
    
    prob_cum = np.zeros(4)
    prob_cum[0] = prob_modified[0]
    for i in range(1,4):
      prob_cum[i] = prob_cum[i-1] + prob_modified[i]
    
    rd = np.random.rand()
    print 'random number is ', rd
    can_check = not can_call
    result = 'CHECK'
    if rd < prob_cum[0]:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        result = 'FOLD'
        print 'folding', result
    elif rd < prob_cum[1]:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        if call_amount < call_limit:
          result = 'CALL:' + str(call_amount)
          print 'calling', result
        else:
          result = 'FOLD'
          print 'folding', result
    elif rd < prob_cum[2]:
      if can_bet:
        # medium bet
        bet_amount = (int([action for action in self.player.legal_actions if 'BET' in action][0].split(':')[1]) + int([action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]))/2
        result = 'BET:' + str(bet_amount)        
        print 'betting', result
      else:
        # medium raise
        raise_amount = (int([action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]) + int([action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]))/2
        result = 'RAISE:' + str(raise_amount)
        print 'raising', result
    else:
      if can_bet:
        # max bet
        result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
        print 'betting', result
      else:
        result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]
        print 'raising', result
    return result
    

  def flop(self, can_raise, can_bet, can_call):
    
    #result = 'CHECK'
    tight_level = 5.0 # inverse of std of the normal distribution, the larger the tighter
    call2pot_limit = 0.3 # max call size to pot size ratio
    conditional_prob_call = 0
    decay_factor = 0.6 # probability of raising decay, affecting raising probability
    num_raise = self.num_of_raise(self.player.last_actions_flop)
    decay = decay_factor ** num_raise
    
    print 'decay factor is ', decay
    
    hole_cards = self.player.hole_cards
    board_cards = self.player.board_cards
    
    idx = evaluator.flop_index(hole_cards[0],hole_cards[1],board_cards[0],board_cards[1],board_cards[2]) 
    
    bucket = self.flop_buckets[idx]
    
    print 'bucket=', bucket
        
    equity = self.cal_equity(bucket)    

    # parameters set by hand    
    if bucket <= 11:
      conditional_prob_call = 0.2
    elif bucket <= 24:
      conditional_prob_call = 0.3
    else:
      conditional_prob_call = 0.5
        
    prob = np.zeros(3)    
    
    prob[2] = sp.norm.cdf(equity, 1, 1.0/tight_level) * 2 * decay
    prob[1] = (1-prob[2]) * conditional_prob_call / decay
    prob[0] = 1 - prob[1] - prob[2]
    
    
    prob_cum = np.zeros(3)
    prob_cum[0] = prob[0]
    for i in range(1,3):
      prob_cum[i] = prob_cum[i-1] + prob[i]

    rd = np.random.rand()
    print 'Random number is', rd
    
    can_check = not can_call
    result = 'CHECK'
    
    print 'Flop Equity:', equity
    print 'Check/Fold prob:',prob[0],', Call Prob:', prob[1], ', Raise Prob:', prob[2]
    
    if rd < prob_cum[0]:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        result = 'FOLD'
        print 'folding', result
    elif rd < prob_cum[1]:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        call2pot = call_amount / self.player.pot_size        
        if call2pot < call2pot_limit:
          result = 'CALL:' + str(call_amount)
          print 'calling', result
        else:
          result = 'FOLD'
          print 'folding', result
    else:
      if can_bet:
        # max bet
        result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
        print 'betting', result
      else:
        result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]
        print 'raising', result
    return result
    
    

  def turn(self, can_raise, can_bet, can_call):
    #result = 'CHECK'
    tight_level = 5.0 # inverse of std of the normal distribution, the larger the tighter
    call2pot_limit = 0.3 # max call size to pot size ratio
    conditional_prob_call = 0
    
    decay_factor = 0.6 # probability of raising decay, affecting raising probability
    num_raise = self.num_of_raise(self.player.last_actions_turn)
    decay = decay_factor ** num_raise
    print 'decay factor is', decay
    
    hole_cards = self.player.hole_cards
    board_cards = self.player.board_cards
    
    idx = evaluator.flop_index(hole_cards[0],hole_cards[1],board_cards[0],board_cards[1],board_cards[2])

    bucket = self.turn_buckets[idx]
    print 'bucket is', bucket
    
    equity = self.cal_equity(bucket)    

    # parameters set by hand    
    if bucket <= 18:
      conditional_prob_call = 0.2
    elif bucket <= 26:
      conditional_prob_call = 0.3
    else:
      conditional_prob_call = 0.5
        
    prob = np.zeros(3)    
    
    prob[2] = sp.norm.cdf(equity, 1, 1.0/tight_level) * 2 * decay 
    prob[1] = (1-prob[2]) * conditional_prob_call / decay
    prob[0] = 1 - prob[1] - prob[2]
    print 'Turn Equity:', equity
    print 'Check/Fold prob:',prob[0],', Call Prob:', prob[1], ', Raise Prob:', prob[2]
    prob_cum = np.zeros(3)
    prob_cum[0] = prob[0]
    for i in range(1,3):
      prob_cum[i] = prob_cum[i-1] + prob[i]

    rd = np.random.rand()
    print 'Random number is', rd
    
    can_check = not can_call
    result = 'CHECK'
    
    if rd < prob_cum[0]:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        result = 'FOLD'
        print 'folding', result
    elif rd < prob_cum[1]:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        call2pot = call_amount / self.player.pot_size        
        if call2pot < call2pot_limit:
          result = 'CALL:' + str(call_amount)
          print 'calling', result
        else:
          result = 'FOLD'
          print 'folding', result
    else:
      if can_bet:
        # max bet
        result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
        print 'betting', result
      else:
        result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]
        print 'raising', result
    return result
    
    
  def river(self, can_raise, can_bet, can_call):
    call2pot_limit = 0.4       
      
    hole_card_str = ''.join(self.player.hole_cards)
    board_card_str = ''.join(self.player.board_cards)
    card_str = hole_card_str +':xx' 
    equity = evaluator.evaluate(card_str, board_card_str, '', 300)
    decay_factor = 0.9 # probability of raising decay, affecting raising probability
    num_raise = self.num_of_raise(self.player.last_actions_river)
    decay = decay_factor ** num_raise    
    
    print 'decay factor is', decay
    
    can_check = not can_call 
    
    
    equity = equity * decay    
    print 'River Equity after decay:', equity
    
    if equity < 0.4:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        result = 'FOLD'
        print 'folding', result
    elif equity < 0.6:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        call2pot = call_amount / self.player.pot_size        
        if call2pot < call2pot_limit:
          result = 'CALL:' + str(call_amount)
          print 'calling', result
        else:
          result = 'FOLD'
          print 'folding', result
    elif equity < 0.8:
      if can_check:
        result = 'CHECK'
        print 'checking', result
      else:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        result = 'CALL:' + str(call_amount)
        print 'calling', result
     
    else:
      if can_bet:
        # max bet
        result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
        print 'betting', result
      elif can_raise:
        if self.player.pot_size < 150:
          result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]
          print 'raising', result
        else:
          call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
          result = 'CALL:' + str(call_amount)
          print 'calling', result
      elif can_call:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        result = 'CALL:' + str(call_amount)
        print 'calling', result
      else:
        print 'error'
    return result
