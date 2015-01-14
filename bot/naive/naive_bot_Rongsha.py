# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot
from lib.evaluator import evaluator

class NaiveBot(base_bot.BaseBot):
  
  def action(self):
    return super(NaiveBot, self).action(self.player.hole_cards,self.player.board_cards,self.player.last_actions,self.player.legal_actions,self.player.player_names)

  def preflop(self, hole_cards,board_cards,last_actions,legal_actions,player_names):
    print '*'*80
    print hole_cards
    print last_actions
    print legal_actions
    print player_names
    raise_flag = 0
    bet_flag = 0
    call_flag = 0
    check_flag = 0
    for action_cand in legal_actions:
      print '+'*50
      print action_cand

      if action_cand[0:4]=='CALL':
        call_action = action_cand;
        call_list = call_action.split(':')
        call_num = call_list[1];
        call_flag = 1;

      elif action_cand[0:5] == 'RAISE':
        raise_list = action_cand.split(':')
        raise_min = raise_list[1];
        raise_min = raise_list[2];
        raise_flag = 1

        raisemin_action = "RAISE:" + raise_min
      elif action_cand[0:3] == 'BET':
        bet_list = action_cand.split(':')
        bet_min = bet_list[1];
        bet_min = bet_list[2];
        bet_flag = 1

        raisemin_action = "BET:" + bet_min
      elif action_cand == 'CHECK':
        check_flag = 1

    print 'call_flag'+str(call_flag)+';  check_flag' + str(check_flag) + \
      ';  raise_flag' + str(raise_flag) + ';  bet_flag' + str(bet_flag)

    if player_names[0] == 'P1':
      betted_num = 0
    elif player_names[1] == 'P1':
      last_act_list = last_actions[0].split(':')
      betted_num = last_act_list[2]
    elif player_names[2] == 'P1':
      last_act_list = last_actions[1].split(':')
      betted_num = last_act_list[2]
 
    player_cards = hole_cards[0]+hole_cards[1] + ":xx:xx"
    board = ""
    dead = ""
    equity = evaluator.evaluate(player_cards, board, dead, 1000)
    if check_flag == 1:
      new_bet_call = 0
    else: # cannot check. Then has call
      new_bet_call = call_num - betted_num;
      if raise_flag == 1: # can raise
        new_bet_raisemin = raise_min - betted_num
      elif bet_flag == 1:
        new_bet_raisemin = bet_min - betted_num
      else: 
        new_bet_raisemin = new_bet_call

    if equity * potsize - (1-equity) * new_bet_call > 0:
      if equity * potsize - (1-equity) * new_bet_raisemin > 0:
        return raisemin_action;
      else:
        return call_action;
    else:
      return 'CHECK' # if cannot check, then automatically fold

    #return 'CHECK'

  def flop(self, *args, **kwargs):
    return 'CHECK'

  def turn(self, *args, **kwargs):
    return 'CHECK'

  def river(self, *args, **kwargs):
    return 'CHECK'
