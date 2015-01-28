# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 01:15:52 2015

@author: zhk
"""

import numpy as np
np.set_printoptions(precision=3, suppress=True)
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)
from lib.evaluator import evaluator_cy, evaluator
from lib import util
from study.cfr import cfr_cy5
import itertools
import time


def exploit_kuhn(node):
  regret = node.dump_regret()
  prob = node.dump_prob()
  root = cfr_cy5.RoundNode(3, 2, 1, 1)
  root.initialize_regret()
  root.load_regret(regret)
  root.load_prob(prob)
  seq1 = np.array([0, 0, 0, 0, 0])
  seq2 = np.array([0, 0, 0, 0, 0])
  util_sb = util_bb = 0.0
  for sb, bb, _ in itertools.permutations([0,1,2]):
    seq1[3] = seq1[4] = sb
    seq2[3] = seq2[4] = bb      
    util_sb_, util_bb_ = root.compute_util(seq1, seq2)
    util_sb += util_sb_
    util_bb += util_bb_
  for i in range(100):
    for sb, bb, _ in itertools.permutations([0,1,2]):
      seq1[3] = seq1[4] = sb
      seq2[3] = seq2[4] = bb      
      util_sb_, util_bb_ = root.compute_best_response(seq1, seq2, True)
  util_sb_after = util_bb_after = 0.0
  for sb, bb, _ in itertools.permutations([0,1,2]):
    seq1[3] = seq1[4] = sb
    seq2[3] = seq2[4] = bb      
    util_sb_, util_bb_ = root.compute_util(seq1, seq2)
    util_sb_after += util_sb_
    util_bb_after += util_bb_  
  util_sb = util_sb / 6
  util_bb = util_bb / 6
  util_sb_after = util_sb_after / 6
  util_bb_after = util_bb_after / 6
  return util_sb, util_sb_after, util_sb_after - util_sb

reload(cfr_cy5)
root = cfr_cy5.RoundNode(3, 2, 1, 1)
root.initialize_regret()
seq1 = np.array([0, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])
cum_time = 0
start_time = time.time()
for i in range(200):
  for sb, bb, _ in itertools.permutations([0,1,2]):
    seq1[3] = seq1[4] = sb
    seq2[3] = seq2[4] = bb
    root.run_cfr(seq1, seq2)
  if time.time() - start_time > 0.0001:
    cum_time += time.time() - start_time
    before, after, exploit = exploit_kuhn(root)
    print i, cum_time, before, after, exploit
    start_time = time.time()


print 'sb: root              ', root.child_nodes[0].average_prob[0:6]
print 'bb: sb check          ', root.child_nodes[0].child_nodes[0].average_prob[0:6]
print 'bb: sb raise          ', root.child_nodes[0].child_nodes[1].average_prob[0:6]
print 'sb: sb check, bb raise', root.child_nodes[0].child_nodes[0].child_nodes[1].average_prob[0:6]
