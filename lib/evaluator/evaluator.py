# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 02:24:21 2015

@author: zhk
"""

#cdef extern from "evaluator_lib.c":
#    unsigned int evaluate_nums(unsigned int b, unsigned int c, unsigned int d, unsigned int e, unsigned int f, unsigned int g)

from lib.evaluator import pbots_calc
from lib.evaluator import evaluator_cy

def evaluate(player_cards, board, dead, num_evaluation=1000000):
	#TODO: revert to num_evaluation
  result = pbots_calc.calc(player_cards, board, dead, 1000)
  return result.ev[0]

def evaluate_turn(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_):
  result = np.array(evaluator_cy.evaluate_turn(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_))
  mean = np.mean(result)
  var = np.var(result)
  bucket = 0
  return mean, var, bucket
