# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot

class NaiveBot(base_bot.BaseBot):
  
  def action(self):
    return super(NaiveBot, self).action()

  def preflop(self, *args, **kwargs):
    return 'CHECK'

  def flop(self, *args, **kwargs):
    return 'CHECK'

  def turn(self, *args, **kwargs):
    return 'CHECK'

  def river(self, *args, **kwargs):
    return 'CHECK'
