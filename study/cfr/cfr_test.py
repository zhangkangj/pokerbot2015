# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 23:15:08 2015

@author: zhk
"""

import ctypes
import multiprocessing
import numpy as np
np.set_printoptions(precision=3, suppress=True)
import time
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)

from lib.evaluator import evaluator_cy, evaluator
from study.cfr import cfr_cy4

root = cfr_cy4.RoundNode(0, 0, 300, 300)
root.initialize_regret()
root.load_regret('data/regret_300_total.npy')
root.load_prob('data/prob_300_total.npy')

n = 4
result = np.reshape(normalize(root.child_nodes[0].average_prob[:(n*169)], n=n), (169,n))
for i in range(51):
  for j in range(i+1, 52):
    idx = evaluator_cy.preflop_idx(i, j)
    print util.n2c([i,j]), idx, result[idx]
