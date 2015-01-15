# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 16:36:02 2015

@author: zhk
"""

import numpy as np
cimport numpy as np
#from libc.math cimport
#from libc.stdlib cimport max, min
from lib import util

'''
Preflop functions
'''
def preflop(card1, card2):
  cdef:
    int c1, c2
  c1 = util.card_to_num(card1)
  c2 = util.card_to_num(card2)
  return preflop_c(c1, c2)

cdef int preflop_c(int c1, int c2):
  cdef:
    int result, r1, r2
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


'''
Flop functions
'''

from evaluator_c cimport evaluate_flop as evaluate_flop_c
  
cdef int flop_idx(int c1, int c2, int c3, int c4, int c5):
  cdef int index, hole_index, board_index
  if c1 > c2:
    hole_index = c1 * (c1 - 1) / 2 + c2
  else:
    hole_index = c2 * (c2 - 1) / 2 + c1
  if c3 < c4:
    c3, c4 = c4, c3
  if c4 < c5:
    c4, c5 = c5, c4
  if c3 < c4:
    c3, c4 = c4, c3
  board_index = c3 * (c3-1) * (c3-2) / 6 + c4 * (c4-1) / 2 + c5
  return hole_index * 22100 + board_index

def evaluate_flop(mc1_, mc2_, bc1_, bc2_, bc3_, num_iter=100):
  cdef:
    unsigned int mc1, mc2, bc1, bc2, bc3
    np.ndarray[np.uint32_t, ndim=1] result = np.zeros(1081, dtype=np.uint32)
    unsigned int* result_ptr = <unsigned int*> result.data
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  bc1 = util.card_to_num(bc1_)
  bc2 = util.card_to_num(bc2_)
  bc3 = util.card_to_num(bc3_)
  evaluate_flop_c(mc1, mc2, bc1, bc2, bc3, num_iter, result_ptr)
  mean = np.mean(result) / 2.0 / num_iter
  var = np.var(result) / 4.0 / num_iter / num_iter
  return mean, var


'''
Turn functions
'''
from evaluator_c cimport evaluate_turn as evaluate_turn_c

def evaluate_turn(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_):
  cdef:
    unsigned int mc1, mc2, bc1, bc2, bc3, bc4
    np.ndarray[np.uint32_t, ndim=1] result = np.zeros(46, dtype=np.uint32)
    unsigned int* result_ptr = <unsigned int*> result.data
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  bc1 = util.card_to_num(bc1_)
  bc2 = util.card_to_num(bc2_)
  bc3 = util.card_to_num(bc3_)
  bc4 = util.card_to_num(bc4_)
  evaluate_turn_c(mc1, mc2, bc1, bc2, bc3, bc4, result_ptr)
  mean = np.mean(result) / 2.0 / 990
  var = np.var(result) / 4.0 / 990 / 990
  return mean, var