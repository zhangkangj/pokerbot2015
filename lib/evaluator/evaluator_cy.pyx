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

from .. import util
from evaluator_c cimport evaluate_nums
from evaluator_c cimport evaluate_river as evaluate_river_c
from evaluator_c cimport evaluate_turn as evaluate_turn_c

def evaluate_cards(a, b, c, d, e, f, g):
  aa = util.card_to_num(a)
  bb = util.card_to_num(b)
  cc = util.card_to_num(c)
  dd = util.card_to_num(d)
  ee = util.card_to_num(e)
  ff = util.card_to_num(f)
  gg = util.card_to_num(g)
  return evaluate_nums(aa, bb, cc, dd, ee, ff, gg)

def evaluate_river(mc1_, mc2_, bc1_, bc2_, bc3_, bc4_, bc5_, num_iter=100):
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
  result = range(46)
  for i in range(46):
    result[i] = result_ptr[i]
  with nogil:
    free(result_ptr)
  return result
    
