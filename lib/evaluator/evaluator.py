# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 02:24:21 2015

@author: zhk
"""

import numpy as np

from lib import util
from lib.evaluator import pbots_calc, evaluator_cy

def evaluate(player_cards, board, dead, num_iter=1000):
  result = pbots_calc.calc(player_cards, board, dead, num_iter)
  return result.ev[0]

def evaluate_preflop(mc1_, mc2_, num_iter=1000):
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  mc1 = util.num_to_card(mc1_)
  mc2 = util.num_to_card(mc2_)
  bucket = evaluator_cy.preflop_idx(mc1, mc2)
  mean = evaluate(mc1+mc2+':xx', '', '', num_iter)
  return result, mean

def evaluate_cards(a, b, c, d, e, f, g):
  aa = util.card_to_num(a)
  bb = util.card_to_num(b)
  cc = util.card_to_num(c)
  dd = util.card_to_num(d)
  ee = util.card_to_num(e)
  ff = util.card_to_num(f)
  gg = util.card_to_num(g)
  return evaluator_cy.evaluate_cards(aa, bb, cc, dd, ee, ff, gg)

def evaluate_flop(mc1_, mc2_, bc1_, bc2_, bc3_, num_iter=100):
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  bc1 = util.card_to_num(bc1_)
  bc2 = util.card_to_num(bc2_)
  bc3 = util.card_to_num(bc3_)
  result = np.ctypeslib.as_array(evaluator_cy.evaluate_flop(mc1, mc2, bc1, bc2, bc3, num_iter))
  mean = np.mean(result) / 2.0 / num_iter
  var = np.var(result) / 4.0 / num_iter / num_iter
  bucket = evaluator_cy.flop_bucket(mean, var)
  return bucket, mean, var

def evaluate_turn(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_):
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  bc1 = util.card_to_num(bc1_)
  bc2 = util.card_to_num(bc2_)
  bc3 = util.card_to_num(bc3_)
  bc4 = util.card_to_num(bc4_)
  result = np.ctypeslib.as_array(evaluator_cy.evaluate_turn(mc1, mc2, bc1, bc2, bc3, bc4))
  mean = np.mean(result) / 990.0 / 2
  var = np.var(result) / 990.0 / 990.0 / 4
  bucket = evaluator_cy.turn_bucket(mean, var)
  return bucket, mean, var

def evaluate_river(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_, bc5_):
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  bc1 = util.card_to_num(bc1_)
  bc2 = util.card_to_num(bc2_)
  bc3 = util.card_to_num(bc3_)
  bc4 = util.card_to_num(bc4_)
  bc5 = util.card_to_num(bc5_)  
  mean = evaluator_cy.evaluate_river(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
  bucket = round(mean * 100) / 16
  return bucket, mean
