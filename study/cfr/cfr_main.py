# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 15:37:03 2015

@author: zhk
"""

import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)
from study.cfr import cfr_cy

reload(cfr_cy)
root = cfr_cy.RoundNode(0, 0, 300, 300)
print root.traverse(0)
print root.traverse(1)
print root.traverse(2)
print root.traverse(3)