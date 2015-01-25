

class Mixedoppnew7Param(object):

  def __init__(self):
    pass

  def readin_params(self):

    param_file_path = '../../massplay/mass_params.txt'

    f = open(param_file_path, 'r')
    # f = open('../../massive_params.txt', 'r')
    lineStr = f.readline()
    print "param lineStr: " + str(lineStr)
    f.close()

    line = lineStr.rstrip().split(', ')
    print "parsed param list: " + str(line)

    # Assign values
    self.river_min_to_bet_mid = float(line[0])
    self.river_min_to_bet_high = float(line[1])
    self.river_min_to_bet_top = float(line[2])
    self.river_max_discount_factor_for_opponent = float(line[3])

    self.turn_min_to_bet_mid = float(line[0]) * 0.95
    self.turn_min_to_bet_high = float(line[1]) * 0.95
    self.turn_min_to_bet_top = float(line[2]) * 0.95
    self.turn_max_discount_factor_for_opponent = float(line[3]) * 0.95

    self.flop_min_to_bet_mid = float(line[0]) * 0.90
    self.flop_min_to_bet_high = float(line[1]) * 0.90
    self.flop_min_to_bet_top = float(line[2]) * 0.90
    self.flop_max_discount_factor_for_opponent = float(line[3]) * 0.90


