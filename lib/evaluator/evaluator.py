# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 02:24:21 2015

@author: zhk
"""

#cdef extern from "evaluator_lib.c":
#    unsigned int evaluate_nums(unsigned int b, unsigned int c, unsigned int d, unsigned int e, unsigned int f, unsigned int g)

from lib.evaluator import pbots_calc

def evaluate(player_cards, board, dead, num_evaluation=1000000):
	#TODO: revert to num_evaluation
  result = pbots_calc.calc(player_cards, board, dead, 1000)
  return result.ev[0]
