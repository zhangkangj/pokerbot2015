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
  LOGPATH = "F:\\Software\\PokerBot\\pokerbot2015\\Analysis\\Casino_Hand\\Day4"
  FILENAME = "Casino_Day-4_Nuts_p_new_2.csv"
  FILEPATH = LOGPATH + "\\" + FILENAME
  df = pd.read_csv(FILEPATH)
  # df['num_of_player_preflop'] = np.sum(df['is_dealer_enter_preflop'], df['is_SB_enter_preflop'], df['is_BB_enter_preflop'])
  df['num_of_player_preflop'] = df['is_dealer_enter_preflop'].astype(int) +df['is_SB_enter_preflop'].astype(int) +df['is_BB_enter_preflop'].astype(int)     
  df['num_of_player_flop'] = df['is_dealer_enter_flop'].astype(int) +df['is_SB_enter_flop'].astype(int) +df['is_BB_enter_flop'].astype(int)     
  df['num_of_player_turn'] = df['is_dealer_enter_turn'].astype(int) +df['is_SB_enter_turn'].astype(int) +df['is_BB_enter_turn'].astype(int)     
  df['num_of_player_river'] = df['is_dealer_enter_river'].astype(int) +df['is_SB_enter_river'].astype(int) +df['is_BB_enter_river'].astype(int)     
  
  df['actual_dealer_equity_preflop'] = (3-df['num_of_player_preflop'])*df['dealer_equity_2']+(df['num_of_player_preflop']-2)*df['dealer_equity_3']
  df['actual_SB_equity_preflop'] = (3-df['num_of_player_preflop'])*df['SB_equity_2']+(df['num_of_player_preflop']-2)*df['SB_equity_3']
  df['actual_BB_equity_preflop'] = (3-df['num_of_player_preflop'])*df['BB_equity_2']+(df['num_of_player_preflop']-2)*df['BB_equity_3']
    
  df['actual_dealer_equity_flop'] = (df['num_player_flop']!=0)*((3-df['num_of_player_flop'])*df['dealer_equity_2_flop']+(df['num_of_player_flop']-2)*df['dealer_equity_3_flop'])
  df['actual_SB_equity_flop'] = (df['num_player_flop']!=0)*((3-df['num_of_player_flop'])*df['SB_equity_2_flop']+(df['num_of_player_flop']-2)*df['SB_equity_3_flop'])
  df['actual_BB_equity_flop'] = (df['num_player_flop']!=0)*((3-df['num_of_player_flop'])*df['BB_equity_2_flop']+(df['num_of_player_flop']-2)*df['BB_equity_3_flop'])
  
  df['actual_dealer_equity_turn'] = (df['num_player_turn']!=0)*((3-df['num_of_player_turn'])*df['dealer_equity_2_turn']+(df['num_of_player_turn']-2)*df['dealer_equity_3_turn'])
  df['actual_SB_equity_turn'] = (df['num_player_turn']!=0)*((3-df['num_of_player_turn'])*df['SB_equity_2_turn']+(df['num_of_player_turn']-2)*df['SB_equity_3_turn'])
  df['actual_BB_equity_turn'] = (df['num_player_turn']!=0)*((3-df['num_of_player_turn'])*df['BB_equity_2_turn']+(df['num_of_player_turn']-2)*df['BB_equity_3_turn'])

  df['actual_dealer_equity_river'] = (df['num_player_river']!=0)*((3-df['num_of_player_river'])*df['dealer_equity_2_river']+(df['num_of_player_river']-2)*df['dealer_equity_3_river'])
  df['actual_SB_equity_river'] = (df['num_player_river']!=0)*((3-df['num_of_player_river'])*df['SB_equity_2_river']+(df['num_of_player_river']-2)*df['SB_equity_3_river'])
  df['actual_BB_equity_river'] = (df['num_player_river']!=0)*((3-df['num_of_player_river'])*df['BB_equity_2_river']+(df['num_of_player_river']-2)*df['BB_equity_3_river'])
  
  
  
  #preflop(df, LOGPATH)

  
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

def AfterPreFlop(df, LogPath):
  Filename = "AfterPreFlop Analysis.csv"
  OutputPath = LogPath + '\\' + Filename
  df = df[df.PreFlop_potsize != 'null']
  df_dealer = df[df.is_dealer_enter_flop]
  df_sb = df[df.is_SB_enter_flop]  
  df_bb = df[df.is_BB_enter_flop]  
  df_dealer['Position'] = 'D'
  df_sb['Position'] = 'SB'
  df_bb['Position'] = 'BB'
  df_dealer = df_dealer[['dealer_name',]]
  
   
  
    
if __name__=="__main__":
  main()