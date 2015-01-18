# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 15:37:03 2015

@author: zhk
"""

import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)
from study.cfr import cfr_cy
from lib.evaluator import evaluator_cy, evaluator
from lib import util

reload(cfr_cy)
root = cfr_cy.RoundNode(0, 0, 300, 300)
root.test_transit(np.array([0, 0, 0, 0, 1]), np.array([0, 0, 0, 0, 0]))
raise_node = root.child_n1odes[0]
print raise_node.child_nodes, raise_node.regret[:2]

seq1 = np.array([0, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])
for i in range(500):
  mc1, mc2, oc1, oc2, bc1, bc2, bc3, bc4, bc5 = np.random.choice(52, 9, replace=True)
  seq1[0] = evaluator_cy.preflop_idx(mc1, mc2)
  seq2[0] = evaluator_cy.preflop_idx(bc1, bc2)
  seq1[1], _, _  = evaluator.evaluate_flop(mc1, mc2, bc1, bc2, bc3)
  seq1[1], _, _  = evaluator.evaluate_flop(oc1, oc2, bc1, bc2, bc3)
  seq1[2], _, _  = evaluator.evaluate_turn(mc1, mc2, bc1, bc2, bc3, bc4)
  seq1[2], _, _  = evaluator.evaluate_turn(oc1, oc2, bc1, bc2, bc3, bc4)
  seq1[3], _ = evaluator.evaluate_river(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
  seq1[3], _ = evaluator.evaluate_river(oc1, oc2, bc1, bc2, bc3, bc4, bc5)
  seq1[4] = evaluator.evaluate_cards(mc1, mc2, bc1, bc2, bc3, bc4, bc4)
  seq2[4] = evaluator.evaluate_cards(oc1, oc2, bc1, bc2, bc3, bc4, bc4)
  root.test_transit(seq1, seq2)
  print

result = np.clip(root.child_nodes[0].regret, 0, np.inf)
print result[46:48]

print evaluator_cy.preflop_idx(8, 29)



