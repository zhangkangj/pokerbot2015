# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 23:21:22 2015

@author: zhk
"""

import time
import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)
from lib.evaluator import evaluator
import multiprocessing

'''
thread_num = 0
result = np.zeros(32587776, dtype=np.int16)
start_time = time.time()
for i in xrange(51):
  for j in xrange(i+1, 52):
    index_first = i + j*(j-1)/2
    for k in xrange(51, 1, -1):
      print i, j, k
      if k==i or k==j:
        continue
      index_second__ = k*(k-1)*(k-2)/6
      for m in range(k-1, 0, -1):
        if m==i or m==j:
          continue
        index_second_ = index_second__ + m*(m-1)/2
        for n in range(m-1, -1, -1):
          if n==i or n==j:
            continue
          index_second = n + index_second_
          index = index_first * 24576 + index_second
          if index % 4 == thread_num:
            bucket, _, _ = evaluator.evaluate_flop(i, j, k, m, n)
            result[index] = bucket
print time.time() - start_time
np.save('data/flop_bucket'+str(thread_num), result)
'''

'''
NUM_THREAD = 4

def gen_turn_bucket(thread_num):
  print 'starting', thread_num
  result = np.zeros(278528*1326, dtype=np.int16)
  start_time = time.time()
  for i in xrange(51):
    for j in xrange(i+1, 52):
      index_first = i + j*(j-1)/2
      for k in xrange(51, 2, -1):
        print i, j, k
        if k==i or k==j:
          continue
        index_second___ = k*(k-1)*(k-2)*(k-3)/24
        for m in xrange(k-1, 1, -1):
          if m==i or m==j:
            continue
          index_second__ = index_second___ + m*(m-1)*(m-2)/6
          for n in xrange(m-1, 0, -1):
            if n==i or n==j:
              continue
            index_second_ = index_second__ + n*(n-1)/2
            for o in xrange(n-1, -1, -1):
              if o==i or o==j:
                continue
              index_second = index_second_ + o
              index = index_first * 278528 + index_second
              assert result[index] == 0, (i, j, k, m, n, o)
              result[index] = 1
              if index % NUM_THREAD == thread_num:
                bucket, _, _ = evaluator.evaluate_turn(i, j, k, m, n, o)
                result[index] = bucket
                pass
  print time.time() - start_time
  np.save('data/turn_bucket'+str(thread_num), result)

processes = []
for i in range(NUM_THREAD):
  print 'creating', i
  p = multiprocessing.Process(target=gen_turn_bucket, args=(i,))
  p.start()
  processes.append(p)
for p in processes:
  p.join()
'''

turn_bucket = np.load('data/evaluator/turn_bucket.npy')
i,j,k,m,n,o=np.random.choice(52, 6, replace=False)
#i,j=sorted([i,j])
#k,m,n,o = sorted([k,m,n,o])
#index = (i+j*(j-1)/2)*278528 + o*(o-1)*(o-2)*(o-3)/24 + n*(n-1)*(n-2)/6 + m*(m-1)/2 + k
turn_index = evaluator.turn_index(i,j,k,m,n,o)
print turn_index, evaluator.evaluate_turn(i,j,k,m,n,o), turn_bucket[turn_index]
