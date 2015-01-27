# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 02:24:45 2015

@author: zhk
"""

import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs': np.get_include()}, reload_support=True)

from lib.evaluator import evaluator