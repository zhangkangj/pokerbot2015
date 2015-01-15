# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 15:24:30 2015

@author: zhk
"""

cdef extern from "evaluator_lib.c":
  unsigned int evaluate_nums(unsigned int a, unsigned int b, unsigned int c,
                             unsigned int d, unsigned int e, unsigned int f,
                             unsigned int g)
  void evaluate_flop(unsigned int mc1, unsigned int mc2,
                     unsigned int bc1, unsigned int bc2, unsigned int bc3,
                     unsigned int num_iter, unsigned int* result)
  void evaluate_turn(unsigned int mc1, unsigned int mc2,
                     unsigned int bc1, unsigned int bc2, unsigned int bc3, unsigned int bc4,
                     unsigned int* result)
  float evaluate_river(unsigned int mc1_, unsigned int mc2_,
                       unsigned int bc1_, unsigned int bc2_, unsigned int bc3_, unsigned int bc4_, unsigned int bc5_)
