

class MixedparamParam(object):

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
    # self.mid_band_factor = float(line[0])
    # self.preflop_raise_lim = float(line[1])
    # self.flop_mid_card_lim = float(line[2])
    # self.river_mid_card_lim = float(line[3])

    self.mid_band_factor = 0.625
    self.preflop_raise_lim = 15.5
    self.flop_mid_card_lim = 0.5
    self.river_mid_card_lim = 0.625

