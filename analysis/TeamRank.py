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
  LOGPATH = "F:\\Software\\PokerBot\\pokerbot2015\\Analysis\\Casino_Result\\Day4"
  FILENAME = "Casino_Day-4_Nuts_p_teams_new.csv"
  FILEPATH = LOGPATH + "\\" + FILENAME
  df = pd.read_csv(FILEPATH)
  
  team_rank = []
  rank = getRank(df)
  num_of_teams = len(rank)-1
  for i in range(num_of_teams):  
    lastTeam_str = rank.ix[len(rank)-1]
    team_rank.insert(0, lastTeam_str)    
    df = df[df.win != lastTeam_str]
    df = df[df.loss != lastTeam_str]
    rank = getRank(df)
  
  print team_rank
    

def getRank(df):
  df['win_score']=1
  df['loss_score'] = -1
  df_win = df[['win','win_score']]
  df_win = df_win.rename(columns={"win":"Team","win_score":"Score"})
  df_loss = df[['loss','loss_score']]
  df_loss = df_loss.rename(columns = {"loss":"Team","loss_score":"Score"})  
  df = df_win.append(df_loss)
  result = df.groupby('Team',as_index=False).sum().sort(['Score'], ascending= False)
  result = result.reset_index()[['Team','Score']]
  return result['Team']

    
if __name__=="__main__":
  main()