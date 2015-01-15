# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 16:36:02 2015

@author: zhk
"""

#from libc.math cimport
#from libc.stdlib cimport max, min
from .. import util
from ..evaluator import evaluator

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

cdef extern from "evaluator_lib.c":
  unsigned int evaluate_nums(unsigned int a, unsigned int b, unsigned int c,
                             unsigned int d, unsigned int e, unsigned int f,
                             unsigned int g)
  void evaluate_flop(unsigned int mc1, unsigned int mc2, unsigned int bc1, unsigned int bc2, unsigned int bc3,
                     unsigned int num_iter, unsigned int* result)

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
