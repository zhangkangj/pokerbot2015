# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 11:45:09 2015

@author: zhk
"""

#import numpy as np
#cimport numpy as np
#from libc.math cimport
cimport cython
from libc.stdlib cimport calloc, free

import ctypes
from .. import util
from evaluator_c cimport evaluate_nums
from evaluator_c cimport evaluate_river as evaluate_river_c
from evaluator_c cimport evaluate_turn as evaluate_turn_c
from evaluator_c cimport evaluate_flop as evaluate_flop_c

def preflop_idx(unsigned int c1, unsigned int c2):
  cdef unsigned int r1, r2, result
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

def flop_idx(int c1, int c2, int c3, int c4, int c5):
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

def evaluate_cards(a, b, c, d, e, f, g):
  cdef:
    unsigned int aa, bb, cc, dd, ee, ff, gg
  aa = util.card_to_num(a)
  bb = util.card_to_num(b)
  cc = util.card_to_num(c)
  dd = util.card_to_num(d)
  ee = util.card_to_num(e)
  ff = util.card_to_num(f)
  gg = util.card_to_num(g)
  return evaluate_nums(aa, bb, cc, dd, ee, ff, gg)

def evaluate_river(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_, bc5_):
  cdef:
    unsigned int mc1, mc2, bc1, bc2, bc3, bc4, bc5
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  bc1 = util.card_to_num(bc1_)
  bc2 = util.card_to_num(bc2_)
  bc3 = util.card_to_num(bc3_)
  bc4 = util.card_to_num(bc4_)
  bc5 = util.card_to_num(bc5_)
  return evaluate_river_c(mc1, mc2, bc1, bc2, bc3, bc4, bc5)

def evaluate_turn(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_):
  cdef:
    unsigned int mc1, mc2, bc1, bc2, bc3, bc4, i
    unsigned int* result_ptr = <unsigned int*> calloc(46, cython.sizeof(int))
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  bc1 = util.card_to_num(bc1_)
  bc2 = util.card_to_num(bc2_)
  bc3 = util.card_to_num(bc3_)
  bc4 = util.card_to_num(bc4_)
  evaluate_turn_c(mc1, mc2, bc1, bc2, bc3, bc4, result_ptr)
  result = (ctypes.c_uint * 46)()
  for i in range(46):
    result[i] = result_ptr[i]
  with nogil:
    free(result_ptr)
  return result

def evaluate_flop(mc1_, mc2_, bc1_, bc2_, bc3_, unsigned int num_iter):
  cdef:
    unsigned int mc1, mc2, bc1, bc2, bc3, i
    unsigned int* result_ptr = <unsigned int*> calloc(1081, cython.sizeof(int))
  mc1 = util.card_to_num(mc1_)
  mc2 = util.card_to_num(mc2_)
  bc1 = util.card_to_num(bc1_)
  bc2 = util.card_to_num(bc2_)
  bc3 = util.card_to_num(bc3_)
  evaluate_flop_c(mc1, mc2, bc1, bc2, bc3, num_iter, result_ptr)
  result = (ctypes.c_uint * 1081)()
  for i in range(1081):
    result[i] = result_ptr[i]
  with nogil:
    free(result_ptr)
  return result