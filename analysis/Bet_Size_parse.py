# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 18:13:49 2015

@author: Arthur Li
"""
import os
#LOGPATH = LOGPATH + Folder + "//"
LOGPATH = "F://Software//PokerBot//pokerbot2015//analysis//Casino_Raw_Data//" 
Folder = 'Day7'
LOGPATH = LOGPATH + Folder + "//"
Team = 'TheCincinnatiKid'
bet_size = []
for file_name in os.listdir(LOGPATH):
  if Team in file_name:
    with open(LOGPATH + file_name) as f:
      for row in f.readlines():
        temp = row.split(' ')
        if temp[0] == Team and (temp[1]=='bets' or temp[1]=='raises'):
          bet_size.append(temp[-1][0:-1])
     
Output_File_Name = "Bet_Size_" + Team + ".txt"
with open(LOGPATH + Output_File_Name,'a') as f:  
  for bet in bet_size:
    try:
      f.write(bet + '  ')    
    except:
      continue
f.close()
       
       