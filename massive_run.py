import numpy
import subprocess
import os
from massplayutil import all_stats, player_stats

# Player name last char cannot be digit
player_names = ["FoldA", "FoldB", "FoldC"]

low_card_up_lim_min = 0.01
low_card_up_lim_max = 0.98
low_card_up_lim_sample_size = 1
low_card_up_lim_paras = list(numpy.linspace(low_card_up_lim_min, low_card_up_lim_max, num=low_card_up_lim_sample_size))

mid_card_up_lim_max = 0.99
mid_card_up_lim_sample_size = 1
# mid_card_up_lim_paras_2d = []

high_card_up_lim_max = 1.0
high_card_up_lim_sample_size = 1
# high_card_up_lim_paras_3d = []

for low_card_up_lim in low_card_up_lim_paras:
  mid_card_up_lim_paras = list(numpy.linspace(low_card_up_lim, mid_card_up_lim_max, num=mid_card_up_lim_sample_size))
  # mid_card_up_lim_paras_2d.append(mid_card_up_lim_paras)
  for mid_card_up_lim in mid_card_up_lim_paras:
      high_card_up_lim_paras = list(numpy.linspace(mid_card_up_lim, high_card_up_lim_max, num=high_card_up_lim_sample_size))
      # high_card_up_lim_paras_3d.append(high_card_up_lim_paras)
      for high_card_up_lim in high_card_up_lim_paras:
        # write the parameter combo to the parameter file
        f = open('massive_params.txt', 'w')
        f.write('%f, %f, %f\n' %(low_card_up_lim, mid_card_up_lim, high_card_up_lim))
        f.close()

        # Create a stats object for the current parameter combo
        all_stats_for_curr_params = all_stats.AllStats(player_names, [low_card_up_lim, mid_card_up_lim, high_card_up_lim])

        # grap the result from the log/test/*.txt files
        result_dir = "./log/test"
        last_line_length = 1000
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
                  lastline = lines[reverselineindex].rstrip()
                  if "Hand #" in lastline:
                    #TODOS                       


                    break
                  reverselineindex = reverselineindex - 1
                fh.close()

                # update the stats 
                all_stats_for_curr_params.update_stats(lastline)
                

                 
          break

# import os
# files = []
# for (dirpath, dirnames, filenames) in os.walk("./log/test"):
#     files.extend(filenames)
#     break

# print "files: " + str(files)


