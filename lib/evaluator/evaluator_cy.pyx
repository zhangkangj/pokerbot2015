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
from evaluator_c cimport evaluate_nums as evaluate_nums_c
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

def flop_bucket(float mean, float var):
  if var < 0.07:
    return min(max(int((mean - 0.1) / 0.075), 0), 11)
  elif var < 0.11:
    return 12 + min(max(int((mean - 0.15) / 0.05), 0), 12)
  elif var < 0.15:
    return 25 + min(max(int((mean - 0.2) / 0.1), 0), 4)
  elif mean < 0.4:
    return 30
  else:
    return 31

def turn_bucket(float mean, float var):
  if var < 0.04:
    return min(max(int((mean - 0.05) / 0.05), 0), 18)
  elif var < 0.09:
    return 19 + min(max(int((mean - 0.1) / 0.075), 0), 7)
  elif var < 0.15:
    return 27 + min(max(int((mean - 0.2) / 0.1), 0), 4)
  elif mean < 0.4:
    return 30
  else:
    return 31

def evaluate_cards(unsigned int a, unsigned int b,
                   unsigned int c, unsigned int d, unsigned int e, unsigned int f, unsigned int g):
  return evaluate_nums_c(a, b, c, d, e, f, g)

def evaluate_river(unsigned int mc1, unsigned int mc2,
                   unsigned int bc1, unsigned int bc2, unsigned int bc3, unsigned int bc4, unsigned int bc5):
  return evaluate_river_c(mc1, mc2, bc1, bc2, bc3, bc4, bc5)

def evaluate_turn(unsigned int mc1, unsigned int mc2,
                  unsigned int bc1, unsigned int bc2, unsigned int bc3, unsigned int bc4):
  cdef:
    unsigned int i
    unsigned int* result_ptr = <unsigned int*> calloc(46, cython.sizeof(int))
  evaluate_turn_c(mc1, mc2, bc1, bc2, bc3, bc4, result_ptr)
  result = (ctypes.c_uint * 46)()
  for i in range(46):
    result[i] = result_ptr[i]
  with nogil:
    free(result_ptr)
  return result

def evaluate_flop(unsigned int mc1, unsigned int mc2,
                  unsigned int bc1, unsigned int bc2, unsigned int bc3,
                  unsigned int num_iter):
  cdef:
    unsigned int i
    unsigned int* result_ptr = <unsigned int*> calloc(1081, cython.sizeof(int))
  evaluate_flop_c(mc1, mc2, bc1, bc2, bc3, num_iter, result_ptr)
  result = (ctypes.c_uint * 1081)()
  for i in range(1081):
    result[i] = result_ptr[i]
  with nogil:
    free(result_ptr)
  return result
