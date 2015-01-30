import numpy
import subprocess
import os
from massplayutil import all_stats, player_stats


def writeAllStats(all_stats_tuples, result_output_file):
  # Sort all the result by the number of wins of the player of interest
  # sorted_all_stats_tuple_list = sorted(all_stats_tuples, key=lambda x: (x[1], x[2]), reverse=True)
  # sort will sort by each of the element of its tuple member by default 
  sorted_all_stats_tuple_list = sorted(all_stats_tuples, reverse=True)

  # Write result to a file
  with open(result_output_file, 'w') as f:
    for all_stats_tuple in sorted_all_stats_tuple_list:
      all_stats_str = all_stats_tuple[2]
      param_list = all_stats_tuple[3]
      f.write('%s, %s\n' % (all_stats_str, str(param_list)))

def writeOneStats(stats_tuple, one_stats_output_file):
  # Write result to a file
  with open(one_stats_output_file, 'a') as f:
    stats_str = stats_tuple[2]
    param_list = stats_tuple[3]
    f.write('%s, %s\n' % (stats_str, str(param_list)))

def generateAllStatsTuple(result_dir, player_list, params_list, name_of_interest):
    # generate stats from the *.txt files in the result dir
  all_stats_for_curr_params = generateAllStats(result_dir, player_names)
  
  # - Use the total win for the current param combo for the player of interest, as 1st sort key 
  player_win = all_stats_for_curr_params.get_player_win_total(name_of_interest)
    # - Use the total win for the current param combo for the player of interest, as 1st sort key 
  player_total_end_stack = all_stats_for_curr_params.get_player_end_stack_total(name_of_interest)
  
  # - Use the total stats info for all player after all games for the current param combo as value
  curr_param_stats_str = all_stats_for_curr_params.output()
  all_stats_tuple = (player_win, player_total_end_stack, curr_param_stats_str, param_list)
  return all_stats_tuple

def generateAllStats(result_dir, player_list):
    # Create a stats object for the current parameter combo
  stats = all_stats.AllStats(player_list)

  # grap the result from the log/test/*.txt files
  # last_line_length = 1000
  for (dirpath, dirnames, filenames) in os.walk(result_dir):
    for filename in filenames:
      if filename.endswith(".txt"):
        with open(result_dir + "/" + filename, 'rb') as fh:
          
          # find the line for the last hand of the game 
          reverselineindex = -1  
          lines = fh.readlines()
          # print "lines:" + str(lines)
          lastline = ""
          while True:
            # find the line indicating the last hand - not precise
            lastline = lines[reverselineindex].rstrip()
            if "Hand #" in lastline:
              break
            reverselineindex = reverselineindex - 1
          fh.close()

          # update the stats 
          stats.update_stats(lastline)

  return stats
          
def generateLinearListExclEnds(min_lim, max_lim, size, deci_precision):
  result_list = [round(y, deci_precision) for y in list(numpy.linspace(min_lim, max_lim, num=(size+2)))]
  result_list = result_list[1:]
  result_list = result_list[:-1]
  return result_list

def getFirstEleAsKey(tuple):
  return tuple[0]

# import os
# files = []
# for (dirpath, dirnames, filenames) in os.walk("./log/test"):
#     files.extend(filenames)
#     break

# print "files: " + str(files)

if __name__ == '__main__':

  import time
  start = time.time()
  game_start = start

  # Player name last char cannot be digit
  player_names = ["MixedOppNewSix", "MixedOppNewNine", "Fold"]

  player_of_interest = "MixedOppNewNine"

  precision = 4

  massplay_result_output_file = "./massplay/mass_result.txt"

  massplay_result_output_file_unsorted = "./massplay/mass_result_unsorted.txt"

  input_params_file = './massplay/mass_params.txt'

  clean_param_file_cmd = "rm -f " + input_params_file

  clean_mass_result_file_cmd = "rm -f " + massplay_result_output_file + " " + massplay_result_output_file_unsorted

  run_result_dir = "./log/test"

  clean_run_result_files_cmd = "rm -fr " + run_result_dir + "/"  + "*.txt"

  engine_cmd = 'java -jar engine.jar'

  # total number of games (which could be a triplicate game on its own) to run 
  total_num_games = 1


  # ---- Variables ----
  # fixed_param_vals = [0.495, 0.7425, 0.8283, 0.105, 
  #   0.495, 0.7425, 0.9142, 0.155, 
  #   0.495, 0.7425, 0.9142, 0.205, 
  #   0.4167, 0.8333, 0.8333, 0.5, 
  #   20.6667, 11.0, 4.0, 4, 2]

  # fixed_param_vals =  [0.0067, 0.4983, 0.8328, 0.105, 
  #   0.6567, 0.8234, 0.9411, 0.155, 
  #   0.3333, 0.6617, 0.7745, 0.205, 
  #   0.4167, 0.8333, 0.8333, 0.5, 
  #   20.667, 11.0, 4.0, 4, 2]   

  #fixed_param_vals = [0.3333, 0.6617, 0.7745, 0.105, 0.3333, 0.6617, 0.8872, 0.155, 0.3333, 0.6617, 0.7745, 0.205, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.3333, 0.6617, 0.7745, 0.105, 0.6567, 0.8234, 0.8823, 0.155, 0.3333, 0.6617, 0.7745, 0.205, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.6567, 0.8234, 0.8823, 0.105, 0.3333, 0.6617, 0.8872, 0.155, 0.6567, 0.8234, 0.9411, 0.205, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.6567, 0.8234, 0.8823, 0.105, 0.6567, 0.8234, 0.8823, 0.155, 0.6567, 0.8234, 0.9411, 0.205, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.3333, 0.6617, 0.8308, 0.105, 0.6567, 0.8234, 0.9117, 0.155, 0.1717, 0.5808, 0.7904, 0.205, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.3333, 0.6617, 0.8308, 0.105, 0.3333, 0.6617, 0.8308, 0.155, 0.495, 0.7425, 0.8713, 0.205, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.1717, 0.5808, 0.7904, 0.105, 0.8183, 0.9042, 0.9521, 0.155, 0.8183, 0.9042, 0.9521, 0.205, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.3333, 0.6617, 0.8308, 0.105, 0.6567, 0.8234, 0.9117, 0.155, 0.1717, 0.5808, 0.7904, 0.205, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #manual
  #fixed_param_vals = [0.5, 0.6617, 0.8308, 0.105, 0.5, 0.6617, 0.8308, 0.1, 0.495, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.5, 0.6617, 0.8308, 0.105, 0.4, 0.6617, 0.8308, 0.1, 0.3, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #fixed_param_vals = [0.5, 0.6617, 0.8308, 0.105, 0.3, 0.6617, 0.8308, 0.1, 0.2, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4, 2]

  #win mixed + stronger
  #fixed_param_vals = [0.5, 0.6617, 0.8308, 0.105, 0.1083, 0.6617, 0.8308, 0.1, 0.4033, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]

  #fixed_param_vals = [0.5, 0.6617, 0.8308, 0.105, 0.305, 0.6617, 0.8308, 0.1, 0.4033, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]

  #fixed_param_vals = [0.5, 0.6617, 0.8308, 0.105, 0.5017, 0.6617, 0.8308, 0.1, 0.4033, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]

  # fixed_param_vals = [0.5, 0.6617, 0.9667, 0.105, 0.4, 0.6617, 0.8333, 0.1, 0.3, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]
  # fixed_param_vals = [0.5, 0.6617, 0.8667, 0.105, 0.4, 0.6617, 0.8667, 0.1, 0.3, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]
  # fixed_param_vals = [0.5, 0.6617, 0.9, 0.105, 0.4, 0.6617, 0.9333, 0.1, 0.3, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]
  # fixed_param_vals = [0.5, 0.6617, 0.8333, 0.105, 0.4, 0.6617, 0.8667, 0.1, 0.3, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]
  
  # what mixedoppnew6 uses
  #fixed_param_vals = [0.5, 0.6617, 0.9667, 0.105, 0.4, 0.6617, 0.8333, 0.1, 0.3, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]
  fixed_param_vals = [0.1355, 0.6617, 0.9667, 0.105, 0.4, 0.6617, 0.8333, 0.1, 0.3, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]
  
  # River
  #0
  sample_size = 1
  if fixed_param_vals != None:
    river_low_card_up_lim_paras = [float(fixed_param_vals[0])]
  else:
    total_num_games *= sample_size
    river_low_card_up_lim_paras = generateLinearListExclEnds(0.01, 0.98, sample_size, precision)
  # TODO: temp tune key 
  # sample_size = 10
  # total_num_games *= sample_size
  # river_low_card_up_lim_paras = generateLinearListExclEnds(0.01, 0.7, sample_size, precision)

  #1
  river_mid_card_up_lim_max = 0.99
  river_mid_card_up_lim_sample_size = 1
  if fixed_param_vals != None:
    river_mid_card_up_lim_paras = [float(fixed_param_vals[1])] 
  else:
    total_num_games *= river_mid_card_up_lim_sample_size

  #2
  river_high_card_up_lim_max = 1.0
  river_high_card_up_lim_sample_size = 2
  if fixed_param_vals != None:
    river_high_card_up_lim_paras = [float(fixed_param_vals[2])]  
  else:
    total_num_games *= river_high_card_up_lim_sample_size

  #3
  sample_size = 1
  if fixed_param_vals != None:
    river_opp_discount_lim_paras = [float(fixed_param_vals[3])]
  else:  
    total_num_games *= sample_size
    river_opp_discount_lim_paras = generateLinearListExclEnds(0.01, 0.2, sample_size, precision)  

  # Turn
  #4
  sample_size = 1
  if fixed_param_vals != None:
    turn_low_card_up_lim_paras = [float(fixed_param_vals[4])]
  else:
    total_num_games *= sample_size
    turn_low_card_up_lim_paras = generateLinearListExclEnds(0.01, 0.6, sample_size, precision)
  
  # # TODO: temp tune key 
  # sample_size = 3
  # total_num_games *= sample_size
  # turn_low_card_up_lim_paras = generateLinearListExclEnds(0.01, 0.6, sample_size, precision)

  #5
  turn_mid_card_up_lim_max = 0.99
  turn_mid_card_up_lim_sample_size = 1
  if fixed_param_vals != None:
    turn_mid_card_up_lim_paras = [float(fixed_param_vals[5])] 
  else:
    total_num_games *= turn_mid_card_up_lim_sample_size

  #6
  turn_high_card_up_lim_max = 1.0
  turn_high_card_up_lim_sample_size = 2
  if fixed_param_vals != None:
    turn_high_card_up_lim_paras = [float(fixed_param_vals[6])]
  else:
    total_num_games *= turn_high_card_up_lim_sample_size

  #7
  sample_size = 1
  if fixed_param_vals != None:
    turn_opp_discount_lim_paras = [float(fixed_param_vals[7])]
  else:  
    total_num_games *= sample_size
    turn_opp_discount_lim_paras = generateLinearListExclEnds(0.01, 0.3, sample_size, precision)      

  # Flop
  #8
  sample_size = 1
  if fixed_param_vals != None:
    flop_low_card_up_lim_paras = [float(fixed_param_vals[8])]
  else:
    total_num_games *= sample_size
    flop_low_card_up_lim_paras = generateLinearListExclEnds(0.01, 0.98, sample_size, precision)

  # # TODO: temp tune key
  # sample_size = 3
  # total_num_games *= sample_size
  # flop_low_card_up_lim_paras = generateLinearListExclEnds(0.01, 0.6, sample_size, precision)

  #9
  flop_mid_card_up_lim_max = 0.99
  flop_mid_card_up_lim_sample_size = 1
  if fixed_param_vals != None:
    flop_mid_card_up_lim_paras = [float(fixed_param_vals[9])] 
  else:
    total_num_games *= flop_mid_card_up_lim_sample_size

  #10
  flop_high_card_up_lim_max = 1.0
  flop_high_card_up_lim_sample_size = 2
  if fixed_param_vals != None:
    flop_high_card_up_lim_paras = [float(fixed_param_vals[10])]  
  else:
    total_num_games *= flop_high_card_up_lim_sample_size

  #11
  sample_size = 1
  if fixed_param_vals != None:
    flop_opp_discount_lim_paras = [float(fixed_param_vals[11])]
  else:  
    total_num_games *= sample_size
    flop_opp_discount_lim_paras = generateLinearListExclEnds(0.01, 0.4, sample_size, precision)  

  # Other variables
  #12 
  sample_size = 2
  if fixed_param_vals != None:
    mid_card_river_call_limit_paras = [float(fixed_param_vals[12])]
  else:
    total_num_games *= sample_size
    mid_card_river_call_limit_paras = generateLinearListExclEnds(0.25, 0.75, sample_size, precision)

  #13
  sample_size = 2
  if fixed_param_vals != None:
    mid_card_call_limit_paras = [float(fixed_param_vals[13])]
  else:  
    total_num_games *= sample_size
    mid_card_call_limit_paras = generateLinearListExclEnds(0.5, 1, sample_size, precision)

  #14
  sample_size = 3
  if fixed_param_vals != None:
    high_card_river_raise_limit_paras = [float(fixed_param_vals[14])]
  else:  
    total_num_games *= sample_size
    high_card_river_raise_limit_paras = generateLinearListExclEnds(0.5, 1, sample_size, precision)

  #15
  sample_size = 3
  if fixed_param_vals != None:
    high_card_raise_limit_paras = [float(fixed_param_vals[15])]
  else:  
    total_num_games *= sample_size
    high_card_raise_limit_paras = generateLinearListExclEnds(0.25, 1, sample_size, precision)

  #16      
  sample_size = 2
  if fixed_param_vals != None:
    preflop_raise_limit_paras = [float(fixed_param_vals[16])]
  else:  
    total_num_games *= sample_size
    preflop_raise_limit_paras = generateLinearListExclEnds(2, 30, sample_size, precision)

  #17
  sample_size = 1
  if fixed_param_vals != None:
    preflop_suitedhand_call_limit_paras = [float(fixed_param_vals[17])]
  else:  
    total_num_games *= sample_size
    preflop_suitedhand_call_limit_paras = generateLinearListExclEnds(2, 20, sample_size, precision)

  #18
  sample_size = 1
  if fixed_param_vals != None:
    preflop_lowhand_call_limit_paras = [float(fixed_param_vals[18])]
  else:  
    total_num_games *= sample_size
    preflop_lowhand_call_limit_paras = generateLinearListExclEnds(2, 6, sample_size, precision)  

  #19
  # to temporarily relieve from 'too many staic loop' error
  sample_size = 1
  if fixed_param_vals != None:
    preflop_verylowhand_call_limit = float(fixed_param_vals[19])
  else:  
    total_num_games *= sample_size
    # preflop_lowhand_call_limit_paras = generateLinearListExclEnds(2, 6, sample_size, precision)  
    preflop_verylowhand_call_limit_paras = 4

  #20
  # to temporarily relieve from 'too many staic loop' error
  sample_size = 1
  if fixed_param_vals != None:
    preflop_nogoodhand_call_limit = float(fixed_param_vals[20])
  else:  
    total_num_games *= sample_size
    #preflop_lowhand_call_limit_paras = generateLinearListExclEnds(2, 6, sample_size, precision)  
    preflop_nogoodhand_call_limit = 2


  # num of runs
  num_run_per_param_set = 3
  total_num_games *= num_run_per_param_set

  # global result list
  all_stats_tuple_list = []

  # game counter
  total_game_count = 0

  print "========" + "Totally " + str(total_num_games) + " Games (each of which could be a triplicate game) to Run" + "========"
  rm_mass_result = subprocess.call([clean_mass_result_file_cmd], shell=True)
  print "... clean_mass_result_file_cmd:" + str(rm_mass_result) + " ..."

  for river_low_card_up_lim in river_low_card_up_lim_paras:
    if river_mid_card_up_lim_paras == None:
      river_mid_card_up_lim_paras = generateLinearListExclEnds(river_low_card_up_lim, river_mid_card_up_lim_max, river_mid_card_up_lim_sample_size, precision)
    for river_mid_card_up_lim in river_mid_card_up_lim_paras:
      if river_high_card_up_lim_paras == None:
        river_high_card_up_lim_paras = generateLinearListExclEnds(river_mid_card_up_lim, river_high_card_up_lim_max, river_high_card_up_lim_sample_size, precision)         
      for river_high_card_up_lim in river_high_card_up_lim_paras:
        for river_opp_discount_lim in river_opp_discount_lim_paras:

          for turn_low_card_up_lim in turn_low_card_up_lim_paras:
            if turn_mid_card_up_lim_paras == None:
              turn_mid_card_up_lim_paras = generateLinearListExclEnds(turn_low_card_up_lim, turn_mid_card_up_lim_max, turn_mid_card_up_lim_sample_size, precision)
            for turn_mid_card_up_lim in turn_mid_card_up_lim_paras:
              if turn_high_card_up_lim_paras == None:
                turn_high_card_up_lim_paras = generateLinearListExclEnds(turn_mid_card_up_lim, turn_high_card_up_lim_max, turn_high_card_up_lim_sample_size, precision)         
              for turn_high_card_up_lim in turn_high_card_up_lim_paras:
                for turn_opp_discount_lim in turn_opp_discount_lim_paras:    

                  for flop_low_card_up_lim in flop_low_card_up_lim_paras:
                    if flop_mid_card_up_lim_paras == None:
                      flop_mid_card_up_lim_paras = generateLinearListExclEnds(flop_low_card_up_lim, flop_mid_card_up_lim_max, flop_mid_card_up_lim_sample_size, precision)
                    for flop_mid_card_up_lim in flop_mid_card_up_lim_paras:
                      if flop_high_card_up_lim_paras == None:
                        flop_high_card_up_lim_paras = generateLinearListExclEnds(flop_mid_card_up_lim, flop_high_card_up_lim_max, flop_high_card_up_lim_sample_size, precision)         
                      for flop_high_card_up_lim in flop_high_card_up_lim_paras:
                        for flop_opp_discount_lim in flop_opp_discount_lim_paras:

                          for mid_card_river_call_limit in mid_card_river_call_limit_paras:
                            for mid_card_call_limit in mid_card_call_limit_paras:
                              for high_card_river_raise_limit in high_card_river_raise_limit_paras:
                                for high_card_raise_limit in high_card_raise_limit_paras:
                                  for preflop_raise_limit in preflop_raise_limit_paras:
                                    for preflop_suitedhand_call_limit in preflop_suitedhand_call_limit_paras:
                                      for preflop_lowhand_call_limit in preflop_lowhand_call_limit_paras:
                                        # for preflop_verylowhand_call_limit in preflop_verylowhand_call_limit_paras:
                                          #   for preflop_nogoodhand_call_limit in preflop_nogoodhand_call_limit_paras:



                                              # -- Clean up before running 
                                              rm_param_result = subprocess.call([clean_param_file_cmd], shell=True)
                                              print "... clean_param_file_cmd:" + str(rm_param_result) + " ..."
                                              rm_run_result = subprocess.call([clean_run_result_files_cmd], shell=True)
                                              print "... clean_run_result_files_cmd:" + str(rm_run_result) + " ..."


                                              # -- Parameters
                                              param_list = [river_low_card_up_lim, river_mid_card_up_lim, river_high_card_up_lim, river_opp_discount_lim,
                                                turn_low_card_up_lim, turn_mid_card_up_lim, turn_high_card_up_lim, turn_opp_discount_lim,
                                                flop_low_card_up_lim, flop_mid_card_up_lim, flop_high_card_up_lim, flop_opp_discount_lim,
                                                mid_card_river_call_limit, mid_card_call_limit, high_card_river_raise_limit, high_card_raise_limit,
                                                preflop_raise_limit, preflop_suitedhand_call_limit, preflop_lowhand_call_limit, preflop_verylowhand_call_limit,
                                                preflop_nogoodhand_call_limit]
                                              print "... parameter combo: " + str(param_list) + "..."

                                              # -- Write the parameter combo to the parameter file
                                              f = open(input_params_file, 'w')
                                              f.write('%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n' %(
                                                river_low_card_up_lim, river_mid_card_up_lim, river_high_card_up_lim, river_opp_discount_lim,
                                                turn_low_card_up_lim, turn_mid_card_up_lim, turn_high_card_up_lim, turn_opp_discount_lim,
                                                flop_low_card_up_lim, flop_mid_card_up_lim, flop_high_card_up_lim, flop_opp_discount_lim,
                                                mid_card_river_call_limit, mid_card_call_limit, high_card_river_raise_limit, high_card_raise_limit,
                                                preflop_raise_limit, preflop_suitedhand_call_limit, preflop_lowhand_call_limit, preflop_verylowhand_call_limit,
                                                preflop_nogoodhand_call_limit))
                                              f.close()

                                              # -- Run engine, the player will read the file above 
                                              # number of times you ran for each set of parameter combo          
                                              for i in range(num_run_per_param_set):
                                                engine_run_result = subprocess.call([engine_cmd], shell=True)
                                                print "......... " + str(i) + " - engine_run_result:" + str(engine_run_result) + ", " + str(param_list) + "..."
                                                
                                                # Print out game count
                                                total_game_count += 1
                                                game_end = time.time()
                                                print "============ " + str(total_game_count) + " Out of " + str(total_num_games) + " Games Has Completed, Duration:" + str(game_end - game_start) + "============" 
                                                game_start = game_end

                                              # -- Generate the result
                                              # generate the tuple for all stats of current param based on the *.txt files
                                              all_stats_tuple_for_curr_params = generateAllStatsTuple(run_result_dir, player_names, param_list, player_of_interest)
                                              # Add this result to the global result list
                                              all_stats_tuple_list.append(all_stats_tuple_for_curr_params)

                                              # Write this to an unsorted file as we go, in case it stops in the middle of the run
                                              writeOneStats(all_stats_tuple_for_curr_params, massplay_result_output_file_unsorted)



  # Write the result to output file
  writeAllStats(all_stats_tuple_list, massplay_result_output_file)

  end = time.time()
  print "========Total Num Games Run: " + str(total_game_count) + ", Total Time Lapsed: " + str(end - start) + "========" 
