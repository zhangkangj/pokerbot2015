

class Mixedoppnew6Param(object):

  def __init__(self):
    pass

  def readin_params(self):

    line = [0.5, 0.6617, 0.9667, 0.105, 0.4, 0.6617, 0.8333, 0.1, 0.3, 0.7425, 0.8713, 0.05, 0.4167, 0.8333, 0.8333, 0.5, 20.667, 11.0, 4.0, 4.0, 2.0]

    # Assign values
    self.river_min_to_bet_mid = float(line[0])
    self.river_min_to_bet_high = float(line[1])
    self.river_min_to_bet_top = float(line[2])
    self.river_max_discount_factor_for_opponent = float(line[3])

    self.turn_min_to_bet_mid = float(line[4])
    self.turn_min_to_bet_high = float(line[5])
    self.turn_min_to_bet_top = float(line[6])
    self.turn_max_discount_factor_for_opponent = float(line[7])

    self.flop_min_to_bet_mid = float(line[8])
    self.flop_min_to_bet_high = float(line[9])
    self.flop_min_to_bet_top = float(line[10])
    self.flop_max_discount_factor_for_opponent = float(line[11])

    self.mid_card_river_call_limit_factor = float(line[12])
    self.mid_card_call_limit_factor = float(line[13])
    self.high_card_river_raise_limit_factor = float(line[14])
    self.high_card_raise_limit_factor = float(line[15])
    self.preflop_raise_limit = float(line[16])
    self.preflop_suitedhand_call_limit = float(line[17])
    self.preflop_lowhand_call_limit = float(line[18])
    self.preflop_verylowhand_call_limit = float(line[19])
    self.preflop_nogoodhand_call_limit = float(line[20])

    print "-----------------in readin_params(), start-----------------"
    print "river_min_to_bet_mid: " + str(self.river_min_to_bet_mid)
    print "river_min_to_bet_high: " + str(self.river_min_to_bet_high)
    print "river_min_to_bet_top: " + str(self.river_min_to_bet_top)
    print "river_max_discount_factor_for_opponent: " + str(self.river_max_discount_factor_for_opponent)
    print "turn_min_to_bet_mid: " + str(self.turn_min_to_bet_mid)
    print "turn_min_to_bet_high: " + str(self.turn_min_to_bet_high)
    print "turn_min_to_bet_top: " + str(self.turn_min_to_bet_top)
    print "turn_max_discount_factor_for_opponent: " + str(self.turn_max_discount_factor_for_opponent)
    print "flop_min_to_bet_mid: " + str(self.flop_min_to_bet_mid)
    print "flop_min_to_bet_high: " + str(self.flop_min_to_bet_high)
    print "flop_min_to_bet_top: " + str(self.flop_min_to_bet_top)
    print "flop_max_discount_factor_for_opponent: " + str(self.flop_max_discount_factor_for_opponent)
    print "mid_card_river_call_limit_factor: " + str(self.mid_card_river_call_limit_factor)
    print "mid_card_call_limit_factor: " + str(self.mid_card_call_limit_factor)    
    print "high_card_river_raise_limit_factor: " + str(self.high_card_river_raise_limit_factor)
    print "high_card_raise_limit_factor: " + str(self.high_card_raise_limit_factor)
    print "preflop_raise_limit: " + str(self.preflop_raise_limit)
    print "preflop_suitedhand_call_limit: " + str(self.preflop_suitedhand_call_limit)
    print "preflop_lowhand_call_limit: " + str(self.preflop_lowhand_call_limit)
    print "preflop_verylowhand_call_limit: " + str(self.preflop_verylowhand_call_limit)
    print "preflop_nogoodhand_call_limit: " + str(self.preflop_nogoodhand_call_limit)
    print "-----------------in readin_params(), end-----------------"