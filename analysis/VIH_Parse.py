# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 18:13:49 2015

@author: Arthur Li
"""


def VIH(LOGPATH, Folder, Team_1, Team_2, other_team, sequence):
  LOGPATH = LOGPATH + Folder + "//"
  File_Front = "MiniTournament_Mini-Tournament-Round-2"
  sys = "_vs_"
  Team_researched = 'Nuts'
  pot_size_limit=150
  if sequence == 1:
    FILENAME_1 = File_Front  + '_' + other_team + sys + Team_1 + sys + Team_2 + ".txt"
    FILENAME_2 = File_Front  + '_' + other_team + sys + Team_2 + sys + Team_1 + ".txt"
  elif sequence == 2:
    FILENAME_1 = File_Front  + "_" + Team_1 + sys + Team_2 + sys + other_team + ".txt"
    FILENAME_2 = File_Front  + "_" + Team_2 + sys + Team_1 + sys + other_team + ".txt"  
  else:
    FILENAME_1 = File_Front  + "_" + Team_1 + sys + other_team + sys + Team_2 + ".txt"
    FILENAME_2 = File_Front  + "_" + Team_2 + sys + other_team + sys + Team_1 + ".txt"
  
  str_list_1 = []
  str_list_2 = []
  index_list = []
  with open(LOGPATH + FILENAME_1,'r') as f:
    count = 0
    stack_last = 0
    stack_diff = 0
    count_can_store = False
    for row in f.readlines():
      if '6.176 MIT Pokerbots' in row:
        continue
      elif row[0:8] == "Hand #1,":
        temp_str = row
        stack_diff = 0
        stack_current = 200
        stack_last = 200
      elif row[0:4] != "Hand": 
        temp_str = temp_str + '\r\n' + row
        if 'wins the pot' in row:
          pot_size = int(row.split(' ')[4][1:-2])
          if pot_size > pot_size_limit and count not in index_list:
            count_can_store = True            
      else:
        str_list_1.append(temp_str)
        temp_str = row
        temp_p = row.split(' ').index(Team_researched) + 1
        stack_current = int(row.split(' ')[temp_p][1:-2])
        stack_diff = abs(stack_current - stack_last)
        stack_last = stack_current
        if stack_diff > pot_size_limit/2-5 and count_can_store:
          index_list.append(count)
          count_can_store = False
        count += 1
    
  with open(LOGPATH + FILENAME_2,'r') as f:
    count = 0
    for row in f.readlines():
      if '6.176 MIT Pokerbots' in row:
        continue
      elif row[0:8] == "Hand #1,":
        temp_str = row
        stack_diff = 0
        stack_last = 200
      elif row[0:4] != "Hand": 
        temp_str = temp_str + '\r\n' + row
        if 'wins the pot' in row:
          pot_size = int(row.split(' ')[4][1:-2])
          if pot_size > pot_size_limit and count not in index_list and stack_diff > pot_size_limit/2-5:
            index_list.append(count)
      else:
        str_list_2.append(temp_str)
        temp_str = row
        temp_p = row.split(' ').index(Team_researched) + 1
        stack_current = int(row.split(' ')[temp_p][1:-2])
        stack_diff = abs(stack_current - stack_last)
        stack_last = stack_current
        count += 1
   
  Output_File_Name = "VIH_" + Team_1 + "_vs_"+ Team_2 + ".txt"
  with open(LOGPATH + Output_File_Name,'a') as f:  
    for index in index_list:
      try:
        f.write('**************************************************************\r\n')
        f.write(str_list_1[index])    
        f.write(str_list_2[index])    
        f.write('**************************************************************\r\n')
      except:
        continue
  f.close()
       
       
       
LOGPATH = 'F://Software//PokerBot//pokerbot2015//analysis//Casino_Raw_Data//'

Oppo_bots = ['CJK','Pokermon','q','kerbopots']
Team_list = []

with open('F://Software//PokerBot//pokerbot2015//analysis//Team_List.txt','r') as f:
  for row in f.readlines():
    Team_list.append(row[0:-1])

for Oppo_team in Oppo_bots:
  for other_team in Team_list:
    if Oppo_team != other_team:
      VIH(LOGPATH,'Mini-t-1', 'Nuts', Oppo_team, other_team,1)        
      VIH(LOGPATH,'Mini-t-1', 'Nuts', Oppo_team, other_team,2)
      VIH(LOGPATH,'Mini-t-1', 'Nuts', Oppo_team, other_team,3)