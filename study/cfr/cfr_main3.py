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
import time

flop_bucket = np.load('data/evaluator/flop_bucket.npy')
turn_bucket = np.load('data/evaluator/turn_bucket.npy')

def normalize(array, n):
  array = np.clip(array, 0, np.inf) + 1e-10
  coeff = np.empty(array.size)
  coeff[0::n] = array[::n]
  for i in range(1, n):
    coeff[0::n] += array[i::n]
  for i in range(1, n):
    coeff[i::n] = coeff[0::n]
  return array/coeff

def bucket_sequence(seq1, seq2):
  mc1, mc2, oc1, oc2, bc1, bc2, bc3, bc4, bc5 = np.random.choice(52, 9, replace=False)
  seq1[0] = evaluator_cy.preflop_idx(mc1, mc2)
  seq2[0] = evaluator_cy.preflop_idx(oc1, oc2)
  seq1[1] = flop_bucket[evaluator_cy.flop_idx(mc1, mc2, bc1, bc2, bc3)]
  seq2[1] = flop_bucket[evaluator_cy.flop_idx(oc1, oc2, bc1, bc2, bc3)]
  seq1[2] = turn_bucket[evaluator_cy.turn_idx(mc1, mc2, bc1, bc2, bc3, bc4)]
  seq2[2] = turn_bucket[evaluator_cy.turn_idx(oc1, oc2, bc1, bc2, bc3, bc4)]
  seq1[3], _ = evaluator.evaluate_river(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
  seq2[3], _ = evaluator.evaluate_river(oc1, oc2, bc1, bc2, bc3, bc4, bc5)
  seq1[4] = evaluator.evaluate_cards(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
  seq2[4] = evaluator.evaluate_cards(oc1, oc2, bc1, bc2, bc3, bc4, bc5)
  return seq1, seq2

def exploit(node, n=100):
  regret = node.dump_regret()
  prob = node.dump_prob()
  root = cfr_cy5.RoundNode(0, 0, 10, 10)
  root.initialize_regret()
  root.load_regret(regret)
  root.load_prob(prob)
  seq1 = np.array([0, 0, 0, 0, 0])
  seq2 = np.array([0, 0, 0, 0, 0])
  util_sb = np.zeros(n)
  for i in range(n):
    seq1, seq2 = bucket_sequence(seq1, seq2)
    util_sb[i], _ = root.run_cfr(seq1, seq2)
  for i in range(10000):
    seq1, seq2 = bucket_sequence(seq1, seq2)
    util_sb_, util_bb_ = root.compute_best_response(seq1, seq2, True)
  util_sb_after = np.zeros(n)
  for i in range(n):
    seq1, seq2 = bucket_sequence(seq1, seq2)
    util_sb_after[i], _ = root.run_cfr(seq1, seq2)
  return (np.mean(util_sb), np.std(util_sb)/np.sqrt(n)),\
         (np.mean(util_sb_after), np.std(util_sb_after)/np.sqrt(n))

reload(cfr_cy5)
root = cfr_cy5.RoundNode(0, 0, 10, 10)
root.initialize_regret()
root.load_regret('data/regret4_10_total.npy')
root.load_prob('data/prob4_10_total.npy')
#exploit(root, 100000)

n = 4
result = np.reshape(normalize(root.child_nodes[0].average_prob[:(n*169)], n=n), (169,n))
for i in range(51):
  for j in range(i+1, 52):
    idx = evaluator_cy.preflop_idx(i, j)
    print util.n2c([i,j]), idx, result[idx]





reload(cfr_cy5)
root = cfr_cy5.RoundNode(0, 0, 2, 2)
root.initialize_regret()
seq1 = np.array([90, 0, 0, 0, 0])
seq2 = np.array([0, 0, 0, 0, 0])
#exploit(root, 100000)

mc1, mc2 = 0, 5
oc1, oc2, bc1, bc2, bc3, bc4, bc5 = np.random.choice([x for x in range(52) if x != mc1 and x!= mc2], 7, replace=False)
seq1[0] = evaluator_cy.preflop_idx(mc1, mc2)
seq2[0] = evaluator_cy.preflop_idx(oc1, oc2)
seq1[1] = flop_bucket[evaluator_cy.flop_idx(mc1, mc2, bc1, bc2, bc3)]
seq2[1] = flop_bucket[evaluator_cy.flop_idx(oc1, oc2, bc1, bc2, bc3)]
seq1[2] = turn_bucket[evaluator_cy.turn_idx(mc1, mc2, bc1, bc2, bc3, bc4)]
seq2[2] = turn_bucket[evaluator_cy.turn_idx(oc1, oc2, bc1, bc2, bc3, bc4)]
seq1[3], _ = evaluator.evaluate_river(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
seq2[3], _ = evaluator.evaluate_river(oc1, oc2, bc1, bc2, bc3, bc4, bc5)
seq1[4] = evaluator.evaluate_cards(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
seq2[4] = evaluator.evaluate_cards(oc1, oc2, bc1, bc2, bc3, bc4, bc5)
print seq1, seq2
root.compute_best_response(seq1, seq2, False)
print root.child_nodes[0].average_prob[0:2]
print root.child_nodes[0].regret[0:2]




for i in range(10000):
  seq1, seq2 = bucket_sequence(seq1, seq2)
  util_sb_, util_bb_ = root.compute_best_response(seq1, seq2, False)


n = 2
result = np.reshape(normalize(root.child_nodes[0].average_prob[:(n*169)], n=n), (169,n))
for i in range(51):
  for j in range(i+1, 52):
    idx = evaluator_cy.preflop_idx(i, j)
    print util.n2c([i,j]), idx, result[idx]

