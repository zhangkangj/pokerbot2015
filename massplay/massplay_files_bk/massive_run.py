import numpy
import subprocess
import os
from massplayutil import all_stats, player_stats


def writeAllStats(all_stats_tuples, result_output_file):
  # Sort all the result by the number of wins of the player of interest
  sorted_all_stats_tuple_list = sorted(all_stats_tuples, key=getFirstEleAsKey, reverse=True)

  # Write result to a file
  with open(result_output_file, 'w') as f:
    for all_stats_tuple in sorted_all_stats_tuple_list:
      all_stats_str = all_stats_tuple[1]
      param_list = all_stats_tuple[2]
      f.write('%s, %s\n' % (all_stats_str, str(param_list)))

def writeOneStats(stats_tuple, one_stats_output_file):
  # Write result to a file
  with open(one_stats_output_file, 'a') as f:
    stats_str = stats_tuple[1]
    param_list = stats_tuple[2]
    f.write('%s, %s\n' % (stats_str, str(param_list)))

def generateAllStatsTuple(result_dir, player_list, params_list, name_of_interest):
    # generate stats from the *.txt files in the result dir
  all_stats_for_curr_params = generateAllStats(result_dir, player_names)
  
  # - Use the total win for the current param combo for the player of interest as key, 
  key_player_win = all_stats_for_curr_params.get_player_win_total(name_of_interest)
  # - Use the total stats info for all player after all games for the current param combo as value
  curr_param_stats_str = all_stats_for_curr_params.output()
  all_stats_tuple = (key_player_win, curr_param_stats_str, param_list)
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

  # Player name last char cannot be digit
  player_names = ["MixedOppNewSeven", "MixedOppNewSix", "FoldNew"]

  player_of_interest = "MixedOppNewSeven"

  precision = 4

  massplay_result_output_file = "mass_result.txt"

  massplay_result_output_file_unsorted = "mass_result_unsorted.txt"

  input_params_file = 'massive_params.txt'

  clean_param_file_cmd = "rm -f " + input_params_file

  clean_mass_result_file_cmd = "rm -f " + massplay_result_output_file + " " + massplay_result_output_file_unsorted

  run_result_dir = "./log/test"

  clean_run_result_files_cmd = "rm -fr " + run_result_dir + "/"  + "*.txt"

  engine_cmd = 'java -jar engine.jar'

  # total number of games (which could be a triplicate game on its own) to run 
  total_num_games = 1

  # Variables
  opp_discount_lim_min = 0.01
  opp_discount_lim_max = 0.49
  opp_discount_lim_sample_size = 2
  total_num_games *= opp_discount_lim_sample_size
  opp_discount_lim_paras = [round(y, precision) for y in list(numpy.linspace(opp_discount_lim_min, opp_discount_lim_max, num=opp_discount_lim_sample_size))]

  low_card_up_lim_min = 0.01
  low_card_up_lim_max = 0.98
  low_card_up_lim_sample_size = 2
  total_num_games *= low_card_up_lim_sample_size
  low_card_up_lim_paras = [round(x, precision) for x in list(numpy.linspace(low_card_up_lim_min, low_card_up_lim_max, num=low_card_up_lim_sample_size))]

  mid_card_up_lim_max = 0.99
  mid_card_up_lim_sample_size = 2
  total_num_games *= mid_card_up_lim_sample_size
  # mid_card_up_lim_paras_2d = []

  high_card_up_lim_max = 1.0
  high_card_up_lim_sample_size = 2
  total_num_games *= high_card_up_lim_sample_size
  # high_card_up_lim_paras_3d = []

  num_run_per_param_set = 2
  total_num_games *= num_run_per_param_set


  # global result list
  all_stats_tuple_list = []

  # game counter
  total_game_count = 0

  print "========" + "Totally " + str(total_num_games) + " Games (each of which could be a triplicate game) to Run" + "========"
  rm_mass_result = subprocess.call([clean_mass_result_file_cmd], shell=True)
  print "... clean_mass_result_file_cmd:" + str(rm_mass_result) + " ..."

  for low_card_up_lim in low_card_up_lim_paras:
    mid_card_up_lim_paras = [round(x, precision) for x in list(numpy.linspace(low_card_up_lim, mid_card_up_lim_max, num=mid_card_up_lim_sample_size))]
    for mid_card_up_lim in mid_card_up_lim_paras:
      high_card_up_lim_paras = [round(x, precision) for x in list(numpy.linspace(mid_card_up_lim, high_card_up_lim_max, num=high_card_up_lim_sample_size))]
      for high_card_up_lim in high_card_up_lim_paras:
        for opp_discount_lim in opp_discount_lim_paras:
          # -- Clean up before running 
          rm_param_result = subprocess.call([clean_param_file_cmd], shell=True)
          print "... clean_param_file_cmd:" + str(rm_param_result) + " ..."
          rm_run_result = subprocess.call([clean_run_result_files_cmd], shell=True)
          print "... clean_run_result_files_cmd:" + str(rm_run_result) + " ..."


          # -- Parameters
          param_list = [low_card_up_lim, mid_card_up_lim, high_card_up_lim, opp_discount_lim]
          print "... parameter combo: " + str(param_list) + "..."

          # -- Write the parameter combo to the parameter file
          f = open(input_params_file, 'w')
          f.write('%f, %f, %f, %f\n' %(low_card_up_lim, mid_card_up_lim, high_card_up_lim, opp_discount_lim))
          f.close()

          # -- Run engine, the player will read the file above 
          # number of times you ran for each set of parameter combo          
          for i in range(num_run_per_param_set):
            engine_run_result = subprocess.call([engine_cmd], shell=True)
            print "......... " + str(i) + " - engine_run_result:" + str(engine_run_result) + ", " + str(param_list) + "..."
            
            # Print out game count
            total_game_count += 1
            print "============ " + str(total_game_count) + " Out of " + str(total_num_games) + " Games Has Completed." + "============" 

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
