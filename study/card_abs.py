# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 14:48:21 2015

@author: zhk
"""

import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include(), 'lib/evaluator']}, reload_support=True, inplace=True)

from lib.evaluator import evaluator