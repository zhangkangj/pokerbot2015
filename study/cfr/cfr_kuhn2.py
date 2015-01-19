# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 20:01:11 2015

@author: zhk
"""

import numpy as np
np.set_printoptions(precision=3, suppress=True)
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)
from study.cfr import cfr_cy2
import itertools


def normalize(array):
  array = np.clip(array, 0, np.inf) + 1e-10
  coeff = np.empty(array.size)
  coeff[::2] = array[::2] + array[1::2]
  coeff[1::2] = coeff[0::2]
  return array/coeff

reload(cfr_cy2)

# ordered cards

root = cfr_cy2.RoundNode(3, 2, 1, 1)
root.initialize_regret()
seq1 = np.array([0, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])
for i in range(1000000):
  util_sb = util_bb = 0.0
  for sb, bb, _ in itertools.permutations([0,1,2]):
    seq1[3] = seq1[4] = sb
    seq2[3] = seq2[4] = bb
    root.run_cfr(seq1, seq2)
    if i%1000 == 0:      
      util_sb_, util_bb_ = root.compute_util(seq1, seq2)
      util_sb += util_sb_
      util_bb += util_bb_
  if i%1000 == 0:
    print i, util_sb/6, util_bb/6
print 'sb: root              ', normalize(root.child_nodes[0].average_prob[0:6])
print 'bb: sb check          ', normalize(root.child_nodes[0].child_nodes[0].average_prob[0:6])
print 'bb: sb raise          ', normalize(root.child_nodes[0].child_nodes[1].average_prob[0:6])
print 'sb: sb check, bb raise', normalize(root.child_nodes[0].child_nodes[0].child_nodes[1].average_prob[0:6])

# random cards
root = cfr_cy2.RoundNode(3, 2, 1, 1)
root.initialize_regret()
seq1 = np.array([0, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])
for i in range(1000000):
  sb, bb = np.random.choice(3, 2, replace=False)
  seq1[3] = seq1[4] = sb
  seq2[3] = seq2[4] = bb
  root.run_cfr(seq1, seq2)
  if i%1000 == 999:
    util_sb = util_bb = 0.0
    for sb, bb, _ in itertools.permutations([0,1,2]):
      seq1[3] = seq1[4] = sb
      seq2[3] = seq2[4] = bb
      util_sb_, util_bb_ = root.compute_util(seq1, seq2)
      util_sb += util_sb_
      util_bb += util_bb_
    print i, util_sb/6, util_bb/6
print 'sb: root              ', normalize(root.child_nodes[0].average_prob[0:6])
print 'bb: sb check          ', normalize(root.child_nodes[0].child_nodes[0].average_prob[0:6])
print 'bb: sb raise          ', normalize(root.child_nodes[0].child_nodes[1].average_prob[0:6])
print 'sb: sb check, bb raise', normalize(root.child_nodes[0].child_nodes[0].child_nodes[1].average_prob[0:6])
