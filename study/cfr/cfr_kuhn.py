# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 20:01:11 2015

@author: zhk
"""

import numpy as np
np.set_printoptions(precision=3, suppress=True)
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)
from study.cfr import cfr_cy
import itertools


reload(cfr_cy)

root = cfr_cy.RoundNode(3, 2, 1, 1)
seq1 = np.array([0, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])

seq1[3] = seq1[4] = 1
seq2[3] = seq2[4] = 1
util_sb_, util_bb_ = root.run_cfr(seq1, seq2)
print 'sb: root              ', root.child_nodes[0].regret[0:6]
print 'bb: sb check          ', root.child_nodes[0].child_nodes[0].regret[0:6]
print 'bb: sb raise          ', root.child_nodes[0].child_nodes[1].regret[0:6]
print 'sb: sb check, bb raise', root.child_nodes[0].child_nodes[0].child_nodes[1].regret[0:6]
print util_sb_, util_bb_

seq1[3] = seq1[4] = 1
seq2[3] = seq2[4] = 1
util_sb_, util_bb_ = root.run_cfr(seq1, seq2)
print 'sb: root              ', root.child_nodes[0].regret[0:6]
print 'bb: sb check          ', root.child_nodes[0].child_nodes[0].regret[0:6]
print 'bb: sb raise          ', root.child_nodes[0].child_nodes[1].regret[0:6]
print 'sb: sb check, bb raise', root.child_nodes[0].child_nodes[0].child_nodes[1].regret[0:6]
print util_sb_, util_bb_

seq1[3] = seq1[4] = 1
seq2[3] = seq2[4] = 2
util_sb_, util_bb_ = root.run_cfr(seq1, seq2)
print 'sb: root              ', root.child_nodes[0].regret[0:6]
print 'bb: sb check          ', root.child_nodes[0].child_nodes[0].regret[0:6]
print 'bb: sb raise          ', root.child_nodes[0].child_nodes[1].regret[0:6]
print 'sb: sb check, bb raise', root.child_nodes[0].child_nodes[0].child_nodes[1].regret[0:6]
print util_sb_, util_bb_





def normalize(array):
  array = np.clip(array, 0, np.inf) + 1e-10
  coeff = np.empty(array.size)
  coeff[::2] = array[::2] + array[1::2]
  coeff[1::2] = coeff[0::2]
  return array/coeff

reload(cfr_cy)

root = cfr_cy.RoundNode(3, 2, 1, 1)
seq1 = np.array([0, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])

util_sb_ave = 0
for i in range(100000):
  util_sb = util_bb = 0.0
  for sb, bb, _ in itertools.permutations([0,1,2]):
    seq1[3] = seq1[4] = sb
    seq2[3] = seq2[4] = bb
    util_sb_, util_bb_ = root.run_cfr(seq1, seq2)
    util_sb += util_sb_
    util_bb += util_bb_
  util_sb_ave += util_sb
  if i/100 * 100 == i:
    print i, util_sb/6, util_bb/6, (util_sb_ave/(i+1)/6 + 1./18) * 18




print 'sb: root              ', root.child_nodes[0].average_prob[0:6]
print 'bb: sb check          ', root.child_nodes[0].child_nodes[0].average_prob[0:6]
print 'bb: sb raise          ', root.child_nodes[0].child_nodes[1].average_prob[0:6]
print 'sb: sb check, bb raise', root.child_nodes[0].child_nodes[0].child_nodes[1].average_prob[0:6]
