# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot
from lib.evaluator import evaluator

class NaivelxBot(base_bot.BaseBot):

  def action(self):
    hole_card_str = ''.join(self.player.hole_cards)
    board_card_str = ''.join(self.player.board_cards)
    card_str = hole_card_str+':xx'*(self.player.num_active_player-1)
    equity = evaluator.evaluate(card_str, board_card_str, '', 1000)
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
   # if self.player.num_board_card ==3:
    #  return 'CHECK'
    return super(NaivelxBot, self).action(equity, can_raise, can_bet, can_call)

  def preflop(self, equity, can_raise, can_bet, can_call):

    result = 'CHECK'
    if self.player.num_active_player == 3:
      up = 0.6
      mid = 0.45
      down = 0.37
    else:
      up = 0.75
      mid = 0.59
      down = 0.5


    print "enter preflop(), equity:" + str(equity) + ", for " + str(self.player.num_active_player) + "players: limits: [" + str(down) + ", " + str(mid) + ", " + str(up) + "]"


    if can_bet and equity >= mid and equity < up:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[1]
      print 'betting', result  
    elif can_bet and equity >= up:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
      print 'betting', result
    elif can_raise and equity >= up and self.player.pot_size <= 40:        
      result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]
      print 'raising', result
    elif can_call and equity >= up and self.player.pot_size > 40:        
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)      
      print 'call', call_amount    
    elif can_raise and equity < up and equity >= mid  and self.player.pot_size <=20:        
      result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]
      print 'raising', result
    elif can_call and equity > up and equity >= mid and self.player.pot_size >20:        
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)      
      print 'call', call_amount   
    elif can_call and equity < mid and equity >= down and self.player.pot_size <10:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)
      print 'calling', call_amount
    else:
      result = 'FOLD'
    return result

  def flop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    if self.player.num_active_player == 3:
      up = 0.65
      mid = 0.5
      down = 0.4
    else:
      up = 0.8
      mid = 0.65
      down = 0.5

    print "enter flop(), equity:" + str(equity) + ", for " + str(self.player.num_active_player) + "players: limits: [" + str(down) + ", " + str(mid) + ", " + str(up) + "]"

    upperPotSize = 59
    lowerPotSize= 29
    if can_bet and equity >= mid and equity < up:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[1]
      print 'betting', result  
    elif can_bet and equity >= up:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
      print 'betting', result  
    elif can_raise and equity >= up and self.player.pot_size <=upperPotSize: 
      print "can_raise & equity >=up & potsize < upperpotsize"
      result = 'RAISE:' + str(int([action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]) + int([action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2])/2)
      print 'raising', result
    elif can_call and equity >= up and self.player.pot_size >upperPotSize:        
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)      
      print 'call', call_amount    
    elif can_raise and equity < up and equity >= mid  and self.player.pot_size <=lowerPotSize:        
      result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]
      print 'raising', result
    elif can_call and equity < up and equity >= mid and self.player.pot_size >lowerPotSize:        
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)      
      print 'call', call_amount   
    elif can_call and equity < mid and equity >= down:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      if call_amount/self.player.pot_size < 0.25:
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount
    else: 
      if can_call:
        result = 'FOLD'
    return result

  def turn(self, equity, can_raise, can_bet, can_call):

    result = 'CHECK'
    if self.player.num_active_player == 3:
      up = 0.7
      mid = 0.55
      down = 0.4
    else:
      up = 0.8
      mid = 0.65
      down = 0.5

    print "enter turn(), equity:" + str(equity) + ", for " + str(self.player.num_active_player) + "players: limits: [" + str(down) + ", " + str(mid) + ", " + str(up) + "]"

    upperPotSize = 80
    lowerPotSize= 49
    if can_bet and equity >= mid and equity < up:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[1]
      print 'betting', result  
    elif can_bet and equity >= up:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
      print 'betting', result  
    elif can_raise and equity >= up and self.player.pot_size <=upperPotSize:        
      result = 'RAISE:' + str(int([action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]) + int([action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2])/2)
      print 'raising', result
    elif can_call and equity >= up and self.player.pot_size >upperPotSize:        
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)      
      print 'call', call_amount    
    elif can_raise and equity < up and equity >= mid  and self.player.pot_size <=lowerPotSize:        
      result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]
      print 'raising', result
    elif can_call and equity < up and equity >= mid and self.player.pot_size > lowerPotSize:        
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)      
      print 'call', call_amount   
    elif can_call and equity < mid and equity >= down:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      if call_amount/self.player.pot_size < 0.25:
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount
    else: 
      if can_call:
        result = 'FOLD'
    return result

  def river(self, equity, can_raise, can_bet, can_call):

    result = 'CHECK'
    if self.player.num_active_player == 3:
      up = 0.8
      mid = 0.65
      down = 0.5
    else:
      up = 0.85
      mid = 0.7
      down = 0.5

    print "enter river(), equity:" + str(equity) + ", for " + str(self.player.num_active_player) + "players: limits: [" + str(down) + ", " + str(mid) + ", " + str(up) + "]"

    upperPotSize = 100
    lowerPotSize= 69
    if can_bet and equity >= mid and equity < up:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[1]
      print 'betting', result  
    elif can_bet and equity >= up:
      result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
      print 'betting', result 
    elif can_raise and equity >= up and self.player.pot_size <=upperPotSize:        
      result = 'RAISE:' + str(int([action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]) + int([action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2])/2)
      print 'raising', result
    elif can_call and equity >= up and self.player.pot_size >upperPotSize:        
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)      
      print 'call', call_amount    
    elif can_raise and equity < up and equity >= mid  and self.player.pot_size <=lowerPotSize:        
      result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[1]
      print 'raising', result
    elif can_call and equity < up and equity >= mid and self.player.pot_size >lowerPotSize:        
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      result = 'CALL:' + str(call_amount)      
      print 'call', call_amount   
    elif can_call and equity < mid and equity >= down:
      call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
      if call_amount/self.player.pot_size < 0.2:
        result = 'CALL:' + str(call_amount)
        print 'calling', call_amount
    else: 
      if can_call:
        result = 'FOLD'
    return result
