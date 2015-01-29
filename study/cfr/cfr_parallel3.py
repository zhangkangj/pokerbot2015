# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 15:37:03 2015

@author: zhk
"""

import random
import os
import ctypes
import multiprocessing
import numpy as np
np.set_printoptions(precision=3, suppress=True)
import time
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)

from lib.evaluator import evaluator_cy, evaluator
from study.cfr import cfr_cy4

NUM_THREAD = 4
NUM_ITER = 5000
NUM_GEN = 1000
NUM_NODE = 14688512
STACK_SIZE = 300

def parallel_cfr(index, num_iter, num_gen, initial_regret, initial_prob, final_regret, final_prob):
  print 'creating root', index, num_iter, num_gen
  root = cfr_cy4.RoundNode(0, 0, STACK_SIZE, STACK_SIZE)
  root.initialize_regret()
  root.load_regret(initial_regret)
  root.load_regret(initial_prob)
  regret, prob = run_cfr(root, index, num_iter, num_gen)
  final_regret[:] = regret
  final_prob[:] = prob
  
def run_cfr(root, index, num_iter, num_gen):
  print 'starting', index, num_iter, num_gen
  seq1 = np.array([0, 0, 0, 0, 0])
  seq2 = np.array([0, 0, 0, 0, 0])
  util_sb = util_bb = 0
  start_time = time.time()
  np.random.seed((int(time.time()*1000000) * index)%429496729)
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
    seq1[4] = evaluator.evaluate_cards(mc1, mc2, bc1, bc2, bc3, bc4, bc5)
    seq2[4] = evaluator.evaluate_cards(oc1, oc2, bc1, bc2, bc3, bc4, bc5)
    util_sb_, util_bb_ = root.run_cfr(seq1, seq2)
    util_sb += util_sb_
    util_bb += util_bb_
    if i%100 == 0:
      print num_gen, index, i, time.time()-start_time, util_sb/i, util_bb/i, STACK_SIZE
      start_time = time.time()
  regret = root.dump_regret()
  prob = root.dump_prob()
  return regret, prob
  
def transfer_file(filename):
  rand_name = filename + str(random.randint(0,1000))
  os.system('scp -c blowfish -C -i ~/.ssh/pokerbot.pem data/%s ubuntu@54.205.253.94:data2/%s' % (filename, rand_name))
  os.system('ssh ubuntu@54.205.253.94 "mv data2/%s data2/%s"'%(rand_name, filename))
  
if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='parallel')
  parser.add_argument('-ss', action='store')
  parser.add_argument('-nt', action='store')
  parser.add_argument('-ni', action='store')
  parser.add_argument('-ng', action='store')
  args = parser.parse_args()
  if args.ss is not None:
    STACK_SIZE = int(args.ss)
    root = cfr_cy4.RoundNode(0, 0, STACK_SIZE, STACK_SIZE)
    NUM_NODE = root.dump_prob().size
  if args.nt is not None:
    NUM_THREAD = int(args.nt)
  if args.ni is not None:
    NUM_ITER = int(args.ni)
  if args.ng is not None:
    NUM_GEN = int(args.ng)
  print 'STACK_SIZE=', STACK_SIZE, 'NUM_THREAD=', NUM_THREAD, 'NUM_ITER=', NUM_ITER
  REGRET_FILE = 'regret4_%d_total' % STACK_SIZE
  PROB_FILE = 'prob4_%d_total' % STACK_SIZE
  try:
    os.system('scp -c blowfish -C -i ~/.ssh/pokerbot.pem ubuntu@54.205.253.94:data2/%s data'% (REGRET_FILE + '.npy'))
    os.system('scp -c blowfish -C -i ~/.ssh/pokerbot.pem ubuntu@54.205.253.94:data2/%s data'% (PROB_FILE + '.npy'))
  except:
    print 'no initial files'
  regret = np.zeros(NUM_NODE, dtype=np.float64)
  try:
    regret = np.load(REGRET_FILE+'.npy')
  except:
    pass
  prob = np.zeros(NUM_NODE, dtype=np.float32)
  try:
    prob = np.load(PROB_FILE+'.npy')
  except:
    pass
  print 'initialized'
  
  for i in range(0, NUM_GEN):
    time.sleep(random.randint(0,20))
    processes = []
    results = [(multiprocessing.Array(ctypes.c_double, NUM_NODE), multiprocessing.Array(ctypes.c_float, NUM_NODE)) for j in range(NUM_THREAD)]
    for j in range(NUM_THREAD):
      thread_args = (j, NUM_ITER, i, regret, prob, results[j][0], results[j][1])
      p = multiprocessing.Process(target=parallel_cfr, args=thread_args)
      p.start()
      processes.append(p)
    for p in processes:
      p.join()
    current_regret = np.zeros(NUM_NODE, dtype=np.float64)
    current_prob   = np.zeros(NUM_NODE, dtype=np.float32)
    for j in range(NUM_THREAD):
      current_regret += np.frombuffer(results[j][0].get_obj(), dtype=np.float64)
      current_prob   += np.frombuffer(results[j][1].get_obj(), dtype=np.float32)
    try:
      os.system('scp -c blowfish -C -i ~/.ssh/pokerbot.pem ubuntu@54.205.253.94:data2/%s data'% (REGRET_FILE + '.npy'))
      os.system('scp -c blowfish -C -i ~/.ssh/pokerbot.pem ubuntu@54.205.253.94:data2/%s data'% (PROB_FILE + '.npy'))
      regret = np.load(REGRET_FILE+'.npy')
      prob = np.load(PROB_FILE+'.npy')
    except:
      print 'no initial files here'
    regret += current_regret * 15.0 / float(NUM_THREAD)
    prob   += current_prob   * 15.0 / float(NUM_THREAD)
    np.save(REGRET_FILE, regret)
    np.save(PROB_FILE, prob)
    transfer_file(REGRET_FILE + '.npy')
    transfer_file(PROB_FILE + '.npy')