# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 14:48:21 2015

@author: zhk
"""

def foo(*args):
  print args

def bar(*args):
  foo(*args)

bar(13)