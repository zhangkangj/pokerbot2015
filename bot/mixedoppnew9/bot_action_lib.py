class BotActionLib(object):

  @staticmethod
  def action_equity_call_fold(player, equity, can_raise, can_bet, can_call, call_limit=None):
    #debug
    print "----------> enter action_equity_call_fold(), call_limit:" + str(call_limit)

    result = 'CHECK'
    if can_call:
        call_amount = int([action for action in player.legal_actions if 'CALL' in action][0].split(':')[1])
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

  @staticmethod
  def action_betraise_call_fold(player, equity, can_raise, can_bet, can_call, band_factor, br_action, betraise_limit=None, call_limit=None, use_min=False, use_max=False):
    #debug
    print "----------##> enter action_betraise_call_fold(), band_factor:" + str(band_factor) + ", bet or raise: " + br_action + ", betraise_limit:" + str(betraise_limit) 
    result = 'CHECK'
    # if we are the one to bet, bet not beyond the limit
    br_legal_act = [action for action in player.legal_actions if br_action in action][0]
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
            result=BotActionLib.action_equity_call_fold(player, equity, can_raise, can_bet, can_call, call_limit)
        else: 
            #debug
            print "----------#######>" + "br_legal_min:" + str(br_legal_min) + "< betraise_limit: " + str(betraise_limit) + ", we still have 'room' to bet. so we bet"       
            # if the min amount to bet/raise is still less than the limit we specified, it means that we still have 'room' to bet. so we bet
            actual_br_amount = min(calc_br_amount, betraise_limit)

            # min_expected_raise_amount = player.current_stacksize * 0.1
            # # Given that we want to raise, if the calculated amount is too small, set it to minimum expected amount to raise
            # if actual_br_amount < min_expected_raise_amount:  
            #     actual_br_amount = min_expected_raise_amount
            
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

  @staticmethod
  def action_equity_raise_call(player, equity, can_raise, can_bet, can_call, band_factor, raise_limit, call_limit, use_min=False, use_max=False):
    #debug
    print "----------> enter action_equity_raise_call(), band_factor:" + str(band_factor) + ", raise_limit:" + str(raise_limit) + ", call_limit:" + str(call_limit)   
    result = 'CHECK'   

    print "----------> enter action_equity_raise_call(), player.opp0.all_actions[]: "  + str(player.opp0.all_actions)
    if can_bet:
        result = BotActionLib.action_betraise_call_fold(player, equity, can_raise, can_bet, can_call, band_factor, 'BET', raise_limit, call_limit, use_min, use_max)
    elif can_raise:
        # TODO: temp limit to two reraise only 
        num_raise_limit = 3

        if len(player.opp0.all_actions) == 0:
            print "------------> enter action_equity_raise_call(), all_actions[] is empty, we just started, so we can raise"
            # If we raise less than the limit, raise
            result = BotActionLib.action_betraise_call_fold(player, equity, can_raise, can_bet, can_call, band_factor, 'RAISE', raise_limit, call_limit, use_min, use_max) 
        else: 
            # get actions object in the current state        
            current_state_actions = player.opp0.all_actions[-1]
            if len(current_state_actions.raise_seqs) < num_raise_limit:
                print "------------> enter action_equity_raise_call(), we only raised " + str(len(current_state_actions.raise_seqs)) + " times, so we can raise again"
                # If we raise less than the limit, raise
                result = BotActionLib.action_betraise_call_fold(player, equity, can_raise, can_bet, can_call, band_factor, 'RAISE', raise_limit, call_limit, use_min, use_max)
            else:
                print "------------> enter action_equity_raise_call(), we already raised " + str(len(current_state_actions.raise_seqs)) + " times, so we fall back to call"
                # If we already raised the limited times, fall back to call anything
                result = BotActionLib.action_equity_call_fold(player, equity, can_raise, can_bet, can_call, None)
    elif can_call:
        # This will only happen if we can not reraise any more
        result = BotActionLib.action_equity_call_fold(player, equity, can_raise, can_bet, can_call, call_limit)
    else:
        print "----------> cannot bet raise or call, will check legal actions: " + str(player.legal_actions) + ", action_equity_raise_call()"

    # Otherwise, we just fall back to default 'Check' 
    return result        

  @staticmethod
  def action_equity_raise_call_max(player, equity, can_raise, can_bet, can_call, band_factor, raise_limit, call_limit):
    result = BotActionLib.action_equity_raise_call(player, equity, can_raise, can_bet, can_call, band_factor, raise_limit, call_limit, False, True)
    return result

  @staticmethod
  def action_equity_raise_call_min(player, equity, can_raise, can_bet, can_call, band_factor, raise_limit, call_limit):
    result = BotActionLib.action_equity_raise_call(player, equity, can_raise, can_bet, can_call, band_factor, raise_limit, call_limit, True, False)
    return result

  @staticmethod
  def action_get_top_strategy(player, equity, can_raise, can_bet, can_call, band_factor, top_hand_strategy_idx):
    #debug
    print "------> enter action_get_top_strategy(), equity: " + str(equity) + ", band_factor:" + str(band_factor) + ", top_hand_strategy_idx: " + str(top_hand_strategy_idx)   
    result = 'CHECK'

    if top_hand_strategy_idx == 0:
        #debug
        print "----------> strategy: 'top_check_call'";
        # 'top_check_call': we try to check and will call any amount
        result = BotActionLib.action_equity_call_fold(player, equity, can_raise, can_bet, can_call, None)

    elif top_hand_strategy_idx == 1:
        #debug
        print "----------> strategy: 'top_raise_max'";
        # to confuse the opponent, we will raise to a limit then fall back to call; iscount the equity, will call anything
        result = BotActionLib.action_equity_raise_call_max(player, equity, can_raise, can_bet, can_call, band_factor, None, None)  

    elif top_hand_strategy_idx == 2:
        #debug
        print "----------> strategy: 'top_raise";
        # raise based on equity, since this is top cards, high equity should lead it to close to raise-max strategy
        result = BotActionLib.action_equity_raise_call(player, equity, can_raise, can_bet, can_call, band_factor, None, None)     

    elif top_hand_strategy_idx == 3:
        #debug
        print "----------> strategy: 'top_raise_with_dicounted_high_eq'";
        # to confuse the opponent, we discount lightly the equity to steer it away from looking like max raise; no raise limit; will call anything
        dicounted_raise_band_factor = band_factor * 0.75
        result = BotActionLib.action_equity_raise_call(player, equity, can_raise, can_bet, can_call, dicounted_raise_band_factor, None, None)
    elif top_hand_strategy_idx == 4:
        #debug
        print "----------> strategy: 'top_raise_with_discounted_low_eq'";
        # to confuse the opponent, we discount heavily the equity to steer it away from looking like max raise; no raise limit; will call anything
        dicounted_raise_band_factor = band_factor * 0.4
        result = BotActionLib.action_equity_raise_call(player, equity, can_raise, can_bet, can_call, dicounted_raise_band_factor, None, None)        
    elif top_hand_strategy_idx == 5:
        #debug
        print "----------> strategy: 'top_raise_with_limit'";
        # to confuse the opponent, we will raise to a limit then fall back to call; will call anything
        top_raise_limit = player.current_stacksize * 0.75
        result = BotActionLib.action_equity_raise_call(player, equity, can_raise, can_bet, can_call, band_factor, top_raise_limit, None)  
    elif top_hand_strategy_idx == 6:
        #debug
        print "----------> strategy: 'top_raise_with_limit_discounted_eq'";
        # to confuse the opponent, we will raise to a limit then fall back to call; iscount the equity, will call anything
        dicounted_raise_band_factor = band_factor * 0.75
        top_raise_limit = player.current_stacksize * 0.75
        result = BotActionLib.action_equity_raise_call(player, equity, can_raise, can_bet, can_call, dicounted_raise_band_factor, top_raise_limit, None) 

    else:
        #debug
        print "----------> default strategy: 'top_raise";
        # default strategy is to raise based on equity, since this is top cards, high equity should lead it to close to raise-max strategy
        result = BotActionLib.action_equity_raise_call(player, equity, can_raise, can_bet, can_call, band_factor, None, None)       

    print "------> selected strategy with idx: " + str(top_hand_strategy_idx) + ", result: " + result

    return result

  @staticmethod    
  def random_select_from_list(list):
    import random
    result = random.choice(list)
    return result             

    #debug
    print "----- enter top_card_river()"

  @staticmethod
  def random_get_top_strategy(player, equity, can_raise, can_bet, can_call, band_factor, top_strategy_condidate_list):
    print "--- enter random_get_top_strategy(),"

    top_card_band_factor = 1

    top_strategy_idx = BotActionLib.random_select_from_list(top_strategy_condidate_list)
    result = BotActionLib.action_get_top_strategy(player, equity, can_raise, can_bet, can_call, band_factor, top_strategy_idx)

    print "--- exit random_get_top_strategy(), result: " + result
        
    return result   
