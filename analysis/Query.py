# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 16:51:49 2015

@author: Xiang Li
"""
import os
import numpy as np
import pandas as pd
import csv


def getFileList(p):
  p = str(p)
  if p =="":
    return []
  p = p.replace("/","\\")
  if p[-1]!="\\":
    p = p + "\\"
  a = os.listdir(p)
  res = [x for x in a if os.path.isfile(p+x)]
  return res

def main():
  LOGPATH = "F:\\Software\\PokerBot\\pokerbot2015\\Analysis"
  FILENAME = "Day2.csv"
  FILEPATH = LOGPATH + "\\" + FILENAME
  df = pd.read_csv(FILEPATH)
  preflop(df, LOGPATH)
  
def preflop(df, LogPath):
  Filename = "Preflop Analysis.csv"
  OutputPath = LogPath + "\\" + Filename
  df_dealer = df[['dealer_name','dealer_hole_cards','dealer_equity_3','dealer_actions_preflop']]
  df_sb = df[["SB_name","SB_hole_cards","SB_equity_3","SB_actions_preflop"]]
  df_bb = df[["BB_name","BB_hole_cards","BB_equity_3","BB_actions_preflop"]]
  
  df_dealer = df_dealer.rename(columns= {"dealer_name":"Name","dealer_hole_cards":"Hole_cards","dealer_equity_3":"Equity","dealer_actions_preflop":"Action"})  
  df_sb = df_sb.rename(columns= {"SB_name":"Name","SB_hole_cards":"Hole_cards","SB_equity_3":"Equity","SB_actions_preflop":"Action"}) 
  df_bb = df_bb.rename(columns= {"BB_name":"Name","BB_hole_cards":"Hole_cards","BB_equity_3":"Equity","BB_actions_preflop":"Action"})
  preflop = df_dealer.append(df_sb.append(df_bb))
  preflop = preflop.sort_index(by=["Name","Equity"], ascending = [0,0])
  preflop.to_csv(OutputPath)
  
    
  
    
if __name__=="__main__":
  main()