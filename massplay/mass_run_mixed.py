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
  player_names = ["MixedParam", "Mixed", "Fold"]

  player_of_interest = "MixedParam"

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

  # Variables
  mid_band_factor_min = 0.5
  mid_band_factor_max = 1
  mid_band_factor_sample_size = 3
  total_num_games *= mid_band_factor_sample_size
  mid_band_factor_lim_paras = generateLinearListExclEnds(mid_band_factor_min, mid_band_factor_max, mid_band_factor_sample_size, precision)

  preflop_raise_lim_min = 2
  preflop_raise_lim_max = 20
  preflop_raise_lim_sample_size = 3
  total_num_games *= preflop_raise_lim_sample_size
  preflop_raise_lim_paras = generateLinearListExclEnds(preflop_raise_lim_min, preflop_raise_lim_max, preflop_raise_lim_sample_size, precision)


  flop_mid_card_lim_min = 0.25
  flop_mid_card_lim_max = 0.75
  flop_mid_card_lim_sample_size = 3
  total_num_games *= flop_mid_card_lim_sample_size
  flop_mid_card_lim_paras = generateLinearListExclEnds(flop_mid_card_lim_min, flop_mid_card_lim_max, flop_mid_card_lim_sample_size, precision)

  river_mid_card_lim_min = 0.25
  river_mid_card_lim_max = 0.75
  river_mid_card_lim_sample_size = 3
  total_num_games *= river_mid_card_lim_sample_size
  river_mid_card_lim_paras = generateLinearListExclEnds(river_mid_card_lim_min, river_mid_card_lim_max, river_mid_card_lim_sample_size, precision)

  num_run_per_param_set = 2
  total_num_games *= num_run_per_param_set

  # global result list
  all_stats_tuple_list = []

  # game counter
  total_game_count = 0

  print "========" + "Totally " + str(total_num_games) + " Games (each of which could be a triplicate game) to Run" + "========"
  rm_mass_result = subprocess.call([clean_mass_result_file_cmd], shell=True)
  print "... clean_mass_result_file_cmd:" + str(rm_mass_result) + " ..."

  for mid_band_factor in mid_band_factor_lim_paras:
    for preflop_raise_lim in preflop_raise_lim_paras:
      for flop_mid_card_lim in flop_mid_card_lim_paras:
        for river_mid_card_lim in river_mid_card_lim_paras:
          # -- Clean up before running 
          rm_param_result = subprocess.call([clean_param_file_cmd], shell=True)
          print "... clean_param_file_cmd:" + str(rm_param_result) + " ..."
          rm_run_result = subprocess.call([clean_run_result_files_cmd], shell=True)
          print "... clean_run_result_files_cmd:" + str(rm_run_result) + " ..."


          # -- Parameters
          param_list = [mid_band_factor, preflop_raise_lim, flop_mid_card_lim, river_mid_card_lim]
          print "... parameter combo: " + str(param_list) + "..."

          # -- Write the parameter combo to the parameter file
          f = open(input_params_file, 'w')
          f.write('%f, %f, %f, %f\n' %(mid_band_factor, preflop_raise_lim, flop_mid_card_lim, river_mid_card_lim))
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
