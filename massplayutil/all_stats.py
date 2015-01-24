import player_stats

class AllStats(object):
  def __init__(self, player_list, param_list):
    self.player_list = player_list
    self.param_list = param_list

    self.stats_dict = {}

    for player in self.player_list:
      # add an init PlayerStat to the dictionary
      self.stats_dict[player] = player_stats.PlayerStats(player)

  def output(self):
    outpoutline = ""
    outputline += str(self.param_list)

    #TODO:
    for player_stat in self.stat_dict:
      outputline = player_stat.

    outputline += str(player1.)

  def update_stats(self, last_hand_stack_str):
    game_end_playerstacks = last_hand_stack_str.split(", ")
    print str(game_end_playerstacks)

    # player 1
    game_end_playerstacks1 = game_end_playerstacks[1].rstrip(")").split(" (")
    game_end_player1 = game_end_playerstacks1[0]
    game_end_stack1 = int(game_end_playerstacks1[1])
    # player 2
    game_end_playerstacks2 = game_end_playerstacks[2].rstrip(")").split(" (")
    game_end_player2 = game_end_playerstacks2[0]
    game_end_stack2 = int(game_end_playerstacks2[1])
    # player 3
    game_end_playerstacks3 = game_end_playerstacks[3].rstrip(")").split(" (")
    game_end_player3 = game_end_playerstacks3[0]
    game_end_stack3 = int(game_end_playerstacks3[1])

    max_stack = max([game_end_stack1, game_end_stack2, game_end_stack3])
    min_stack = min([game_end_stack1, game_end_stack2, game_end_stack3])


    # populate the stats for player1
    player1_stat = self.stats_dict[game_end_player1]
    if game_end_stack1 == max_stack:
      player1_stat.win += 1
    elif game_end_stack1 == min_stack:
      player1_stat.third += 1
    else:
      player1_stat.second += 1
    player1_stat.total_game_end_stack += game_end_stack1

    # populate the stats for player2
    player2_stat = self.stats_dict[game_end_player2]
    if game_end_stack2 == max_stack:
      player2_stat.win += 1
    elif game_end_stack2 == min_stack:
      player2_stat.third += 1
    else:
      player2_stat.second += 1
    player2_stat.total_game_end_stack += game_end_stack2

    # populate the stats for player3
    player3_stat = self.stats_dict[game_end_player3]
    if game_end_stack3 == max_stack:
      player3_stat.win += 1
    elif game_end_stack3 == min_stack:
      player3_stat.third += 1
    else:
      player3_stat.second += 1
    player3_stat.total_game_end_stack += game_end_stack3      