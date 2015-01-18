# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:58:46 2015

@author: zhk
"""

from .. import base_bot
from lib.evaluator import evaluator

class Mixed4Bot(base_bot.BaseBot):

  def action(self):
    hole_card_str = ''.join(self.player.hole_cards)
    board_card_str = ''.join(self.player.board_cards)
    card_str = hole_card_str+':xx'*(self.player.num_active_player-1)
    equity = evaluator.evaluate(card_str, board_card_str, '', 100)
    can_raise = False
    can_bet = False
    can_call = False
    for action in self.player.legal_actions:
      can_raise |= 'RAISE' in action
      can_bet |= 'BET' in action
      can_call |= 'CALL' in action
    return super(Mixed4Bot, self).action(equity, can_raise, can_bet, can_call)

  def preflop(self, equity, can_raise, can_bet, can_call):
    result = 'CHECK'
    raise_hand_str = ['AA','KK','QQ','JJ','TT','AK','AQ','AJ','AT','KQ']
    call_hand_str = ['QJ','JT','T9','98','87']
    hole_card_str = ''.join(self.player.hole_cards)
    temp_str1 = hole_card_str[0]+hole_card_str[2]
    temp_str2 = hole_card_str[2]+hole_card_str[0]
    suit_equal = hole_card_str[1] == hole_card_str[3]
    
    is_raise_hand = (temp_str1 in raise_hand_str or temp_str2 in raise_hand_str)
    is_call_hand = (suit_equal and (temp_str1 in call_hand_str or temp_str2 in call_hand_str))
    is_call_hand_low = (temp_str1 in call_hand_str or temp_str2 in call_hand_str)

    #debug
    print "----------look at the hole_cards: " + str(hole_card_str) 
    print "----------FLAGS: is_raise_hand: " + str(is_raise_hand) + ", is_call_hand: " + str(is_call_hand) + ", is_call_hand_low: " + str(is_call_hand_low) 
    print "----------equity: " + str(equity)
    print "----------curr pot_size: " + str(self.player.pot_size)
    print "----------my curr stack: " + str(self.player.current_stacksize)

    if self.player.pot_size <= (self.player.current_stacksize * 0.3):
        #debug
        print "---------- enter <=" + str((self.player.current_stacksize * 0.3))

        if is_raise_hand:
            #debug
            print "---------- enter <=" + str((self.player.current_stacksize * 0.3)) + " raise hand logic: "

            if can_bet:
                result = 'BET:' + [action for action in self.player.legal_actions if 'BET' in action][0].split(':')[2]
                print 'betting', result
            elif can_raise:        
                result = 'RAISE:' + [action for action in self.player.legal_actions if 'RAISE' in action][0].split(':')[2]
                print 'raising', result
            elif can_call:
                call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
                result = 'CALL:' + str(call_amount)
                print 'calling', result
            else:
                print "---------- enter <=" + str((self.player.current_stacksize * 0.3)) + " raise hand; cannot bet, raise, or call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK"
        elif is_call_hand:
            #debug
            print "---------- enter <=" + str((self.player.current_stacksize * 0.3)) + " call hand logic: "

            if can_call:
                call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
                if call_amount <= (self.player.current_stacksize * 0.2):
                    result = 'CALL:' + str(call_amount) 
                    print 'calling', call_amount
                else:
                    result = 'FOLD'
                    print 'folding'
            else:
                print "---------- enter <=" + str((self.player.current_stacksize * 0.3)) + " call hand; cannot call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK"
        elif is_call_hand_low:
            #debug
            print "---------- enter <=" + str((self.player.current_stacksize * 0.3)) + " low call hand logic: "
                     
            if can_call:
                call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])

                if call_amount <= (self.player.current_stacksize * 0.05):

                    #debug
                    print "--------------->  enter <=" + str((self.player.current_stacksize * 0.05)) + " low call hand logic, will call: "
    
                    result = 'CALL:' + str(call_amount) 
                    print 'calling', call_amount
                else:
                    result = 'FOLD'
                    print 'folding'
            else:
                print "---------- enter <=" + str((self.player.current_stacksize * 0.3)) + " low call hand; cannot call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK"
        elif can_call:
            #debug
            print "---------- enter <=" + str((self.player.current_stacksize * 0.3)) + " no good card logic: "

            # no good card, if the call_amount is small enough, continue
            call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
            if call_amount <= (self.player.current_stacksize * 0.02):

                #debug
                print "---------------> enter <=" + str((self.player.current_stacksize * 0.02)) + " no good hand logic, will call: "

                result = 'CALL:' + str(call_amount) 
                print 'calling', call_amount
            else:
                result = 'FOLD'
                print 'folding'
        else:
            #debug
            print "---------- enter <=" + str((self.player.current_stacksize * 0.3)) + " no good hand; cannot call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK" 
    else:
        # if the pot_size is accumulated to too large, it means everyone is raising, we resort to call instead of raise, 
        # to break the potential loop of raising
        if (is_raise_hand or is_call_hand) and can_call:
            #debug
            print "---------- enter >" + str((self.player.current_stacksize * 0.3)) + " raise or call hand: definitely call"

            # if we have good card, definitely call 
            print "-----????? problem here: index out of range. self.player.legal_actions: " + str(self.player.legal_actions)
            call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
            result = 'CALL:' + str(call_amount)
            print 'calling', result 
        elif is_call_hand_low:
            #debug
            print "---------- enter >" + str((self.player.current_stacksize * 0.3)) + " low call hand: "

            # consistent with top half
            if can_call:
                call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
                if call_amount <= (self.player.current_stacksize * 0.05):

                    #debug
                    print "--------------->  enter <=" + str((self.player.current_stacksize * 0.05)) + " low call hand logic, will call: "
           
                    result = 'CALL:' + str(call_amount) 
                    print 'calling', call_amount
                else:
                    result = 'FOLD'
                    print 'folding'
            else:
                print 'For a call-able hand (>20): cannot call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK'    
        elif can_call:
            #debug
            print "---------- enter >" + str((self.player.current_stacksize * 0.3)) + " no good hand: "
                   
            # consistent with top half
            call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
            if call_amount <= (self.player.current_stacksize * 0.02):

                #debug
                print "---------------> enter <=" + str((self.player.current_stacksize * 0.02)) + " no good hand logic, will call: "
                   
                result = 'CALL:' + str(call_amount) 
                print 'calling', call_amount
            else:
                result = 'FOLD'
                print 'folding'
        else:
            print "---------- enter >" + str((self.player.current_stacksize * 0.3)) + " no good hand; cannot call, legal_actions:[' + str(self.player.legal_actions) + '], will CHECK" 
    
        #debug
        print "----------preflop result: " + result
        if result not in self.player.legal_actions:
            print '----------Found illegal action: ' + result + ", legal_actions:" + str(self.player.legal_actions)    

    return result

  def action_equity_call_fold(self, equity, can_raise, can_bet, can_call, call_limit=None):
    #debug
    print "----------> enter action_equity_call_fold(), call_limit:" + str(call_limit)

    result = 'CHECK'
    if can_call:
        call_amount = int([action for action in self.player.legal_actions if 'CALL' in action][0].split(':')[1])
        #debug
        print "----------########> call amount:" + str(call_amount)
        if call_limit is not None:
            if call_amount <= call_limit:
                #debug
                print "----------############> enter <=" + ", call limit specified:" + str(call_limit) + ", call, action_equity_call_fold()"
                result = 'CALL:' + str(call_amount) 
                print 'calling', call_amount
            else:
                #debug
                print "----------############> enter >" + ", call limit specified:" + str(call_limit) + ", fold, action_equity_call_fold()"                        
                result = 'FOLD'
                print 'folding'
        else:
            #debug
            print "----------############>" + ", call limit not specified, call, action_equity_call_fold()"
            result = 'CALL:' + str(call_amount) 
            print 'calling', call_amount
    # Otherwise, we just fall back to default 'Check' 
    return result

  def action_betraise_call_fold(self, equity, can_raise, can_bet, can_call, band_factor, br_action, betraise_limit=None, call_limit=None, use_min=False, use_max=False):
    #debug
    print "----------##> enter action_betraise_call_fold(), band_factor:" + str(band_factor) + ", bet or raise: " + br_action + ", betraise_limit:" + str(betraise_limit) 
    result = 'CHECK'
    # if we are the one to bet, bet not beyond the limit
    br_legal_act = [action for action in self.player.legal_actions if br_action in action][0]
    br_legal_min = int(br_legal_act.split(':')[1])
    br_legal_max = int(br_legal_act.split(':')[2])
    print "----------##> enter action_betraise_call_fold(), br_legal_min:" + str(br_legal_min) + ", br_legal_max: " + str(br_legal_max)

    if use_min:
        calc_br_amount = br_legal_min
    elif use_max:
        calc_br_amount = br_legal_max
    else:
        calc_br_amount = int(equity * (br_legal_max - br_legal_min) * band_factor + br_legal_min)

    #debug
    print "----------####> caculated bet/raise amount:" + str(calc_br_amount) + ", action_betraise_call_fold()"
    if betraise_limit is not None:
        #debug
        print "----------######>" + "betraise_limit specified:" + str(betraise_limit) + ", will " + br_action + ", action_betraise_call_fold()"   
        if br_legal_min >= betraise_limit:
            #debug
            print "----------#######>" + "br_legal_min:" + str(br_legal_min) + ">= betraise_limit: " + str(betraise_limit) + ", will fall back to call"
            # if currently it costs more than our raise bet limit to raise, we reach our limit and fall back to call
            result=self.action_equity_call_fold(equity, can_raise, can_bet, can_call, call_limit)
        else: 
            #debug
            print "----------#######>" + "br_legal_min:" + str(br_legal_min) + "< betraise_limit: " + str(betraise_limit) + ", we still have 'room' to bet. so we bet"       
            # if the min amount to bet/raise is still less than the limit we specified, it means that we still have 'room' to bet. so we bet
            actual_br_amount = min(calc_br_amount, betraise_limit)

            min_expected_raise_amount = self.player.current_stacksize * 0.1
            # Given that we want to raise, if the calculated amount is too small, set it to minimum expected amount to raise
            if actual_br_amount < min_expected_raise_amount:  
                actual_br_amount = min_expected_raise_amount
            
            # extra guard for legal bet/raise
            if actual_br_amount > br_legal_max:
                actual_br_amount = br_legal_max
            elif actual_br_amount < br_legal_min:
                actual_br_amount = br_legal_min

            #debug
            print "----------####> actual bet/raise amount:" + str(calc_br_amount) + ", action_betraise_call_fold()"
            result = br_action + ":" + str(actual_br_amount)
          
    else:
        #debug
        print "----------######>" + "betraise_limit not specified:, will " + br_action + ", action_betraise_call_fold()"        
        # if no limit specified, we bet normally
        actual_br_amount = calc_br_amount
        # extra guard for legal bet/raise
        if actual_br_amount > br_legal_max:
            actual_br_amount = br_legal_max
        elif actual_br_amount < br_legal_min:
            actual_br_amount = br_legal_min
        #debug
        print "----------####> actual bet/raise amount:" + str(calc_br_amount) + ", action_betraise_call_fold()"
        result = br_action + ":" + str(actual_br_amount)

    #debug
    print "----------##> result: " + result + ", exiting action_betraise_call_fold() ..."

    return result 

  def action_equity_raise_call(self, equity, can_raise, can_bet, can_call, band_factor, raise_limit, call_limit, use_min=False, use_max=False):
    #debug
    print "----------> enter action_equity_raise_call(), band_factor:" + str(band_factor) + ", raise_limit:" + str(raise_limit) + ", call_limit:" + str(call_limit)   
    result = 'CHECK'    
    if can_bet:
        result = self.action_betraise_call_fold(equity, can_raise, can_bet, can_call, band_factor, 'BET', raise_limit, call_limit, use_min, use_max)
    elif can_raise:
        result = self.action_betraise_call_fold(equity, can_raise, can_bet, can_call, band_factor, 'RAISE', raise_limit, call_limit, use_min, use_max)
    elif can_call:
        # This will only happen if we can not reraise any more
        result = self.action_equity_call_fold(equity, can_raise, can_bet, can_call, call_limit)
    else:
        print "----------> cannot bet raise or call, will check legal actions: " + str(self.player.legal_actions) + ", action_equity_raise_call()"

    # Otherwise, we just fall back to default 'Check' 
    return result        

  def action_get_top_strategy(self, equity, can_raise, can_bet, can_call, band_factor, top_hand_strategy_idx):
    #debug
    print "------> enter action_get_top_strategy(), equity: " + str(equity) + ", band_factor:" + str(band_factor) + ", top_hand_strategy_idx: " + str(top_hand_strategy_idx)   
    result = 'CHECK'

    if top_hand_strategy_idx == 0:
        #debug
        print "----------> strategy: 'top_check_call'";
        # 'top_check_call': we try to check and will call any amount
        result = self.action_equity_call_fold(equity, can_raise, can_bet, can_call, None)

    elif top_hand_strategy_idx == 1:
        #debug
        print "----------> strategy: 'top_raise_max'";
        # to confuse the opponent, we will raise to a limit then fall back to call; iscount the equity, will call anything
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, band_factor, None, None, False, True)  

    elif top_hand_strategy_idx == 2:
        #debug
        print "----------> strategy: 'top_raise";
        # raise based on equity, since this is top cards, high equity should lead it to close to raise-max strategy
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, band_factor, None, None)     

    elif top_hand_strategy_idx == 3:
        #debug
        print "----------> strategy: 'top_raise_with_dicounted_high_eq'";
        # to confuse the opponent, we discount lightly the equity to steer it away from looking like max raise; no raise limit; will call anything
        dicounted_raise_band_factor = band_factor * 0.75
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, dicounted_raise_band_factor, None, None)
    elif top_hand_strategy_idx == 4:
        #debug
        print "----------> strategy: 'top_raise_with_discounted_low_eq'";
        # to confuse the opponent, we discount heavily the equity to steer it away from looking like max raise; no raise limit; will call anything
        dicounted_raise_band_factor = band_factor * 0.4
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, dicounted_raise_band_factor, None, None)        
    elif top_hand_strategy_idx == 5:
        #debug
        print "----------> strategy: 'top_raise_with_limit'";
        # to confuse the opponent, we will raise to a limit then fall back to call; will call anything
        top_raise_limit = self.player.current_stacksize * 0.75
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, band_factor, top_raise_limit, None)  
    elif top_hand_strategy_idx == 6:
        #debug
        print "----------> strategy: 'top_raise_with_limit_discounted_eq'";
        # to confuse the opponent, we will raise to a limit then fall back to call; iscount the equity, will call anything
        dicounted_raise_band_factor = band_factor * 0.75
        top_raise_limit = self.player.current_stacksize * 0.75
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, dicounted_raise_band_factor, top_raise_limit, None) 

    else:
        #debug
        print "----------> default strategy: 'top_raise";
        # default strategy is to raise based on equity, since this is top cards, high equity should lead it to close to raise-max strategy
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, band_factor, None, None)       

    print "------> selected strategy with idx: " + str(top_hand_strategy_idx) + ", result: " + result

    return result
    
  def random_select_from_list(self, list):
    import random
    result = random.choice(list)
    return result             
 

  def action_equity_high(self, equity, can_raise, can_bet, can_call, band_factor):

    # when we have relative high cards, we raise up to half what we have and will call anything
    high_card_equity_band_factor = band_factor * 1
    high_card_raise_limit = self.player.current_stacksize * 0.5
    high_card_call_limit = None

    #debug
    print "----- enter high_card_equity_band_factor:" + str(high_card_equity_band_factor) + ", high_card_raise_limit:" + str(high_card_raise_limit) + ", high_card_call_limit:" + str(high_card_call_limit)

    result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, high_card_equity_band_factor, high_card_raise_limit, high_card_call_limit)    
    return result

  def action_equity_mid(self, equity, can_raise, can_bet, can_call, band_factor):
    # when the poor_limit is 0.5, almost play as good as Mixed
    poor_limit = self.player.game_init_stack_size * 0.5
    average_limit = self.player.game_init_stack_size * 1.5

    #debug
    print "----- enter action_equity_mid"
    if self.player.current_stacksize < poor_limit:
        # when poor, risk less, but not too little
        poor_call_limit = self.player.game_init_stack_size * 0.1

        #debug
        print "-----> enter action_equity_mid, poor: poor_call_limit:" + str(poor_call_limit)
        # if we lost substantially, we should play very conservatively with midium card - call/fold only
        result = self.action_equity_call_fold(equity, can_raise, can_bet, can_call, poor_call_limit)

    elif (self.player.current_stacksize >= poor_limit) and (self.player.current_stacksize < average_limit):      
        average_equity_band_factor = band_factor * 1
        # just leave half init stack size reserved for our comeback
        average_call_limit = self.player.current_stacksize * 0.7
        # half init stack size reserved for our comeback
        average_raise_limit = average_call_limit/2.1

        #debug
        print "-----> enter average_equity_band_factor:" + str(average_equity_band_factor) + ", average_call_limit:" + str(average_call_limit) + ", average_raise_limit:" + str(average_raise_limit)

        # if we are , play normally
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, average_equity_band_factor, average_raise_limit, average_call_limit)   
    
    else:
        rich_equity_band_factor = band_factor * 1
        # just leave half init stack size reserved for our comeback
        rich_call_limit = self.player.current_stacksize - self.player.game_init_stack_size/2
        # half init stack size reserved for our comeback
        rich_raise_limit = rich_call_limit/2.1

        #debug
        print "-----> enter rich_equity_band_factor:" + str(rich_equity_band_factor) + ", rich_call_limit:" + str(rich_call_limit) + ", rich_raise_limit:" + str(rich_raise_limit)
       
        # if we have won quite a bit, play more aggressively
        result = self.action_equity_raise_call(equity, can_raise, can_bet, can_call, rich_equity_band_factor, rich_raise_limit, rich_call_limit)   
    return result

  def low_card(self, equity, can_raise, can_bet, can_call):
    # between low and mid, use this when we want to 
    # raise small bet to built up the pot and more aggressively 
    # 'open' the opportunity to potentially good card later

    #debug
    print "---- enter low_card()"

    result = 'CHECK'
    # If opponent bets, don't want to follow, have to fold
    if can_call:
      result = 'FOLD' 
    # Otherwise, we just fall back to default 'Check' 
    return result

  # def lower_card(self, equity, can_raise, can_bet, can_call):
  #   #debug
  #   print "---- enter lower_card()"

  #   result = 'CHECK'
  #   # If opponent bets, don't want to follow, have to fold
  #   if can_call:
  #     result = 'FOLD' 
  #   # Otherwise, we just fall back to default 'Check' 
  #   return result

  def mid_card(self, equity, can_raise, can_bet, can_call):
    #debug
    print "---- enter mid_card()"

    mid_card_band_factor = 1
    result = self.action_equity_mid(equity, can_raise, can_bet, can_call, mid_card_band_factor)
    return result

  def high_card(self, equity, can_raise, can_bet, can_call):
    #debug
    print "---- enter high_card()"

    high_card_band_factor = 1
    result = self.action_equity_high(equity, can_raise, can_bet, can_call, high_card_band_factor)   
    return result 

    # 0 - top_check_call
    # 1 - top_raise_max
    # 2 - top_raise
    # 3 - top_raise_with_dicounted_high_eq
    # 4 - top_raise_with_discounted_low_eq
    # 5 - top_raise_with_limit
    # 6 - top_raise_with_limit_discounted_eq  
    # other - top_raise   

  def top_card_flop(self, equity, can_raise, can_bet, can_call):
    #debug
    print "--- enter top_card_flop()"

    top_card_band_factor = 1

    top_strategy_idx = self.random_select_from_list([0,1,2,3,4,5,6])
    result = self.action_get_top_strategy(equity, can_raise, can_bet, can_call, top_card_band_factor, top_strategy_idx)
    
    print "--- exit top_card_flop(), result: " + result

    return result 

  def top_card_turn(self, equity, can_raise, can_bet, can_call):
    #debug
    print "--- enter top_card_turn()"

    top_card_band_factor = 1

    top_strategy_idx = self.random_select_from_list([2,3,5])
    result = self.action_get_top_strategy(equity, can_raise, can_bet, can_call, top_card_band_factor, top_strategy_idx)

    print "--- exit top_card_turn(), result: " + result
        
    return result 
    
  def top_card_river(self, equity, can_raise, can_bet, can_call):
    #debug
    print "----- enter top_card_river()"

    top_card_band_factor = 1

    top_strategy_idx = self.random_select_from_list([1,1,1,2,3,3])
    result = self.action_get_top_strategy(equity, can_raise, can_bet, can_call, top_card_band_factor, top_strategy_idx)

    print "--- exit top_card_river(), result: " + result
        
    return result        

  def flop(self, equity, can_raise, can_bet, can_call):
    #debug
    print "--- enter flop(), equity: " + str(equity)

    #result = 'CHECK'
    # min_to_bet_lower = 0.4
    min_to_bet_mid = 0.4
    min_to_bet_high = 0.7
    min_to_bet_top = 0.8

    #--Low range
    if equity >= 0 and equity < min_to_bet_mid: 
    # if equity >= 0 and equity < min_to_bet_lower: 
    # if equity >= 0 and equity < min_to_bet_lower: 
      result = self.low_card(equity, can_raise, can_bet, can_call)
    # #--Lower range
    # if equity >= min_to_bet_lower and equity < min_to_bet_mid: 
    #   result = self.lower_card(equity, can_raise, can_bet, can_call)
    #--Mid Range
    elif equity >= min_to_bet_mid and equity < min_to_bet_high:
      result = self.mid_card(equity, can_raise, can_bet, can_call)
    #--High Range
    elif equity >= min_to_bet_high and equity < min_to_bet_top:
      result = self.high_card(equity, can_raise, can_bet, can_call)  
    #--Top Range
    elif equity >= min_to_bet_top and equity <= 1.0:
      result = self.top_card_flop(equity, can_raise, can_bet, can_call)

    else:
      print 'ERROR: equity: ', equity, ' is out of legal range - flop()'
    return result

  def turn(self, equity, can_raise, can_bet, can_call):
    #debug
    print "--- enter turn(), equity: " + str(equity)

    #result = 'CHECK'
    min_to_bet = 0.5
    min_to_bet_1 = 0.7
    min_to_bet_2 = 0.8

    #--Low range
    if equity >= 0 and equity < min_to_bet: 
      result = self.low_card(equity, can_raise, can_bet, can_call)
    #--Mid Range
    elif equity >= min_to_bet and equity < min_to_bet_1:
      result = self.mid_card(equity, can_raise, can_bet, can_call)
    #--High Range
    elif equity >= min_to_bet_1 and equity < min_to_bet_2:
      result = self.high_card(equity, can_raise, can_bet, can_call)  
    #--Top Range
    elif equity >= min_to_bet_2 and equity <= 1.0:
      result = self.top_card_turn(equity, can_raise, can_bet, can_call)

    else:
      print 'ERROR: equity: ', equity, ' is out of legal range - turn()'
    return result

  def river(self, equity, can_raise, can_bet, can_call):
    #debug
    print "--- enter river(), equity: " + str(equity)

    min_to_bet = 0.5
    min_to_bet_1 = 0.7
    min_to_bet_2 = 0.8
    
    # We play more aggressively at river if the pot is large enough
    enticing_pot_amount = self.player.game_init_stack_size * 0.75
    limit_discount_for_enticing_pot = 0.05

    if (self.player.pot_size > enticing_pot_amount):
        min_to_bet = (1 - limit_discount_for_enticing_pot) * min_to_bet
        min_to_bet_1 = (1 - limit_discount_for_enticing_pot) * min_to_bet_1
        min_to_bet_2 = (1 - limit_discount_for_enticing_pot) * min_to_bet_2

    #--Low range
    if equity >= 0 and equity < min_to_bet: 
      result = self.low_card(equity, can_raise, can_bet, can_call)
    #--Mid Range
    elif equity >= min_to_bet and equity < min_to_bet_1:
      result = self.mid_card(equity, can_raise, can_bet, can_call)
    #--High Range
    elif equity >= min_to_bet_1 and equity < min_to_bet_2:
      result = self.high_card(equity, can_raise, can_bet, can_call)  
    #--Top Range
    elif equity >= min_to_bet_2 and equity <= 1.0:
      result = self.top_card_river(equity, can_raise, can_bet, can_call)

    else:
      print 'ERROR: equity: ', equity, ' is out of legal range - river()'
    return result
