# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 02:24:21 2015

@author: zhk
"""

import numpy as np
from lib.evaluator import pbots_calc
from lib.evaluator import evaluator_cy

def evaluate(player_cards, board, dead, num_evaluation=1000):
  result = pbots_calc.calc(player_cards, board, dead, num_evaluation)
  return result.ev[0]

def evaluate_preflop(mc1_, mc2_, num_iter=1000):
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  mc1 = util.num_to_card(mc1_)
  mc2 = util.num_to_card(mc2_)
  bucket = evaluator_cy.preflop_idx(mc1, mc2)
  mean = evaluate(mc1+mc2+':xx', '', '', num_iter)
  return result, mean

def evaluate_flop(mc1_, mc2_, bc1_, bc2_, bc3_, num_iter=100):
  result = np.ctypeslib.as_array(evaluator_cy.evaluate_flop(mc1_, mc2_, bc1_, bc2_, bc3_, num_iter))
  mean = np.mean(result) / 2.0 / num_iter
  var = np.var(result) / 4.0 / num_iter / num_iter
  bucket = 0
  return bucket, mean, var

def evaluate_turn(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_):
  result = np.ctypeslib.as_array(evaluator_cy.evaluate_turn(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_))
  mean = np.mean(result) / 990.0 / 2
  var = np.var(result) / 990.0 / 990.0 / 4
  bucket = 0
  return bucket, mean, var

def evaluate_river(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_, bc5_):
  mean = evaluator_cy.evaluate_river(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_, bc5_)
  bucket = 0
  return bucket, mean
