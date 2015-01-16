# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 15:37:03 2015

@author: zhk
"""

import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include()]}, reload_support=True, inplace=True)
from study.cfr import cfr_cy

reload(cfr_cy)
root = cfr_cy.RoundNode(0, None, None, 0, 300, 300)
print root.traverse()
print root.traverse_game_round(0)
print root.traverse_game_round(1)
print root.traverse_game_round(2)
print root.traverse_game_round(3)
print
print root.traverse_pot_greater_than(-1)
print root.traverse_pot_greater_than(10)
print root.traverse_pot_greater_than(100)
print root.traverse_pot_greater_than(600)