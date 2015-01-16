# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 14:48:21 2015

@author: zhk
"""

import matplotlib.pyplot as plt
import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)

from lib.evaluator import evaluator
from lib import util



def onpick(event):
    idx = event.ind
    print cards[idx[0]], means[idx[0]], varis[idx[0]]

evaluator.evaluate_flop(*['Tc', 'Ah', 'Th', '3h', 'Td'])
evaluator.evaluate('Ts7c:xx', '6c7dTh', '')

means = np.zeros(1000)
varis = np.zeros(1000)
cards = []
for i in range(1000):
  nums = np.random.choice(52, 5, replace=False)
  _, means[i], varis[i] = evaluator.evaluate_flop(*nums)
  cards.append(util.n2c(nums))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(means, varis, picker=5)
fig.canvas.mpl_connect('pick_event', onpick)
plt.show()

means = np.zeros(2000)
varis = np.zeros(2000)
cards = []
for i in range(2000):
  nums = np.random.choice(52, 6, replace=False)
  _, means[i], varis[i] = evaluator.evaluate_turn(*nums)
  cards.append(util.n2c(nums))  
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(means, varis, picker=5)
fig.canvas.mpl_connect('pick_event', onpick)
plt.show()

means = np.zeros(10000)
varis = np.zeros(10000)
for i in range(10000):
  _, means[i] = evaluator.evaluate_river(*np.random.choice(52, 7, replace=False))
plt.hist(means)
plt.show()