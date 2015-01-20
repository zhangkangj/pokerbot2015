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


def normalize(array, n):
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
for i in range(1,10000):
  mc1 = 20
  mc2 = 21
  #oc1 = 1
  #oc2 = 19
  #bc1, bc2, bc3, bc4, bc5 = np.random.choice([x for x in range(0,52) if x!=mc1 and x!=mc2 and x!=oc1 and x!=oc2], 5, replace=False)
  oc1, oc2, bc1, bc2, bc3, bc4, bc5 = np.random.choice([x for x in range(0,52) if x!=mc1 and x!=mc2], 7, replace=False)
  seq1[0] = evaluator_cy.preflop_idx(mc1, mc2)
  seq2[0] = evaluator_cy.preflop_idx(oc1, oc2)
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
  if i%100 == 0:
    print i, util_sb/i, util_bb/i
    print 'sb: root    ', np.reshape(root.child_nodes[0].average_prob[:507], (169,3))[evaluator_cy.preflop_idx(mc1, mc2)]
    print 'bb: sb raise', np.reshape(root.child_nodes[0].child_nodes[2].average_prob[:338], (169,2))[evaluator_cy.preflop_idx(0, 21)]
    print 'bb: sb raise', np.reshape(root.child_nodes[0].child_nodes[2].average_prob[:338], (169,2))[evaluator_cy.preflop_idx(mc1, mc2)]    
    print 'bb: sb raise', np.reshape(root.child_nodes[0].child_nodes[2].average_prob[:338], (169,2))[evaluator_cy.preflop_idx(48, 49)]
    print    

# fix cards
print 'sb: root    ', root.child_nodes[0].average_prob[30:33]
print 'bb: sb check', root.child_nodes[0].child_nodes[1].average_prob[:338]
print 'bb: sb raise', np.reshape(root.child_nodes[0].child_nodes[2].average_prob[:338], (169,2))
bb_prob = np.reshape(root.child_nodes[0].child_nodes[2].average_prob[:338], (169,2))
bb_regret = np.reshape(root.child_nodes[0].child_nodes[2].regret[:338], (169,2))
for i in range(51):
  for j in range(i+1, 52):
    idx = evaluator_cy.preflop_idx(i, j)
    print util.n2c([i,j]), idx, bb_prob[idx]#, bb_regret[idx]






root = cfr_cy2.RoundNode(0, 0, 30, 30)
root.initialize_regret()
seq1 = np.array([0, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])
util_sb = util_bb = 0
for i in range(1,100000):
  mc1, mc2, oc1, oc2, bc1, bc2, bc3, bc4, bc5 = np.random.choice(52, 9, replace=False)
  seq1[0] = evaluator_cy.preflop_idx(mc1, mc2)
  seq2[0] = evaluator_cy.preflop_idx(oc1, oc2)
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

n = 3
result = np.reshape(normalize(root.child_nodes[0].average_prob[:(n*169)], n=n), (169,n))
for i in range(51):
  for j in range(i+1, 52):
    idx = evaluator_cy.preflop_idx(i, j)
    print util.n2c([i,j]), idx, result[idx]








# parallel
root = cfr_cy2.RoundNode(0, 0, 4, 4)
root.load_regret('data/regret_300_total.npy')
root.load_prob('data/prob_300_total.npy')
n = 3
result = np.reshape(normalize(root.child_nodes[0].average_prob[:(n*169)], n=n), (169,n))
for i in range(51):
  for j in range(i+1, 52):
    idx = evaluator_cy.preflop_idx(i, j)
    print util.n2c([i,j]), idx, result[idx]