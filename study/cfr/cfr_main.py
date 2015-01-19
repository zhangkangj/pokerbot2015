# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 15:37:03 2015

@author: zhk
"""

import numpy as np
np.set_printoptions(precision=3, suppress=True)
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)
from study.cfr import cfr_cy2
from lib.evaluator import evaluator_cy, evaluator
from lib import util


def normalize(array, n=4):
  array = np.clip(array, 0, np.inf) + 1e-10
  coeff = np.empty(array.size)
  coeff[0::n] = array[::n]
  for i in range(1, n):
    coeff[0::n] += array[i::n]
  for i in range(1, n):
    coeff[i::n] = coeff[0::n]
  return array/coeff

reload(cfr_cy2)

root = cfr_cy2.RoundNode(0, 0, 4, 4)
root.initialize_regret()
seq1 = np.array([0, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])
util_sb = util_bb = 0
for i in range(1,100000):
  mc1, mc2, oc1, oc2, bc1, bc2, bc3, bc4, bc5 = np.random.choice(52, 9, replace=True)
  seq1[0] = evaluator_cy.preflop_idx(mc1, mc2)
  seq2[0] = evaluator_cy.preflop_idx(bc1, bc2)
  seq1[1], _, _  = evaluator.evaluate_flop(mc1, mc2, bc1, bc2, bc3)
  seq2[1], _, _  = evaluator.evaluate_flop(oc1, oc2, bc1, bc2, bc3)
  seq1[2], _, _  = evaluator.evaluate_turn(mc1, mc2, bc1, bc2, bc3, bc4)
  seq2[2], _, _  = evaluator.evaluate_turn(oc1, oc2, bc1, bc2, bc3, bc4)
  seq1[3], _ = evaluator.evaluate_river(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
  seq2[3], _ = evaluator.evaluate_river(oc1, oc2, bc1, bc2, bc3, bc4, bc5)
  seq1[4] = evaluator.evaluate_cards(mc1, mc2, bc1, bc2, bc3, bc4, bc4)
  seq2[4] = evaluator.evaluate_cards(oc1, oc2, bc1, bc2, bc3, bc4, bc4)
  util_sb_, util_bb_ = root.run_cfr(seq1, seq2)
  util_sb += util_sb_
  util_bb += util_bb_
  if i%1000 == 0:
    print i, util_sb/i, util_bb/i

result = np.reshape(normalize(root.child_nodes[0].average_prob[:676]), (169,4), n=3)
for i in range(51):
  for j in range(i+1, 52):
    idx = evaluator_cy.preflop_idx(i, j)
    print util.n2c([i,j]), idx, result[idx]
