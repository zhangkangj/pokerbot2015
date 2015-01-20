# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 15:37:03 2015

@author: zhk
"""

import multiprocessing
import numpy as np
np.set_printoptions(precision=3, suppress=True)
import time
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)

from lib.evaluator import evaluator_cy, evaluator
from study.cfr import cfr_cy2

NUM_THREAD = 32
NUM_ITER = 1000
STACK_SIZE = 300
REGRET_FILE = 'data/regret_300_total' 
PROB_FILE = 'data/prob_300_total'

def run_cfr(args):
  index, initial_regret, initial_prob, num_iter, num_gen = args
  print 'creating root', num_gen, index
  root = cfr_cy2.RoundNode(0, 0, STACK_SIZE, STACK_SIZE)
  print 'created root', index, initial_regret, initial_prob
  if initial_regret is None:
    root.initialize_regret()
  else:
    root.load_regret(initial_regret)
  if initial_prob is not None:
    root.load_regret(initial_prob)
  seq1 = np.array([0, 0, 0, 0, 0])
  seq2 = np.array([0, 0, 0, 0, 0])
  util_sb = util_bb = 0
  print 'starting', index
  start_time = time.time()
  for i in range(1, num_iter):
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
    if i%100 == 0:
      print num_gen, index, i, time.time()-start_time, util_sb/i, util_bb/i
      start_time = time.time()
  regret = root.dump_regret()
  prob = root.dump_prob()
  return regret, prob

initial_regret = None
try:
  initial_regret = np.load(REGRET_FILE+'.npy')
except:
  pass
initial_prob = None
try:
  initial_prob = np.load(PROB_FILE+'.npy')
except:
  pass

if initial_regret is None or initial_prob is None:
  thread_pool = multiprocessing.Pool(NUM_THREAD)
  results = thread_pool.map(run_cfr, [(x, None, None, 5000, 0) for x in range(NUM_THREAD)])
  total_regret, total_prob = results[0]
  for (regret, prob) in results[1:]:
    total_regret += regret
    total_prob   += prob
  total_regret = total_regret * 0.5
  total_prob   = total_prob   * 0.5
  np.save(REGRET_FILE, total_regret)
  np.save(PROB_FILE, total_prob)
else:
  total_regret = initial_regret
  total_prob = initial_prob

for i in range(1, 500):
  thread_pool = multiprocessing.Pool(4)
  results = thread_pool.map(run_cfr, [(x, total_regret, total_prob, NUM_ITER, i) for x in range(NUM_THREAD)])
  total_regret, total_prob = results[0]
  for (regret, prob) in results[1:]:
    total_regret += regret * i**(1/2)
    total_prob   += prob * i**(1/2)
  np.save(REGRET_FILE, total_regret)
  np.save(PROB_FILE, total_prob)
