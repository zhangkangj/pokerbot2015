from .. import base_opponent

class Mixedoppnew8Opponent(base_opponent.BaseOpponent):

  def eval_opponent(self):
    max_opp_eval_limit = 1
    min_opp_eval_limit = 0
    result = float(min_opp_eval_limit)

    #debug
    print "-------------======> enter MixedoppnewOpponent.eval_opponent(), self.oppo_name: " + self.oppo_name + " is an active_player"

    self.is_large_betraise = False
    self.is_small_betraise = False

    self.is_in_checkraise = False    
    self.is_in_checkcall = False
    self.is_in_betraise = False
    self.is_in_betcall = False

    self.is_cross_check_raisebet = False

    self.is_cross_nocheck_nocall_hasraisebet_raisebet = False
    self.is_cross_nocheck_hascall_hasraisebet_raisebet = False
    self.is_cross_nocheck_noraisebet_raisebet = False
    self.is_cross_hascheck_noraisebet_raisebet = False

    # self.state=action_state
    # self.call_seqs=[];
    # self.call_amounts=[];
    # self.raise_seqs=[]
    # self.raise_amounts=[]
    # self.bet_seqs=[]
    # self.bet_amounts=[]
    # self.post_seqs=[]
    # self.post_amounts=[]
    # self.check_seqs=[]
    # self.fold_seqs=[]
    # self.action_count = 0        

    total_betraise_amt = self.total_bet_amount + self.total_raise_amount 
    if total_betraise_amt > self.player.game_init_stack_size * 0.75:
      self.is_large_betraise = True
    elif total_betraise_amt < self.player.game_init_stack_size * 0.05:
      self.is_small_betraise = True

    print "-------------======> in eval_opponent(), self.all_actions: " + str(self.all_actions)
    # last element of the all_action list is the current state actions 
    curr_actions = self.all_actions[-1]
    if curr_actions is None or curr_actions is '':
      print "Error: Current action is empty or None"
      return 0

    # in-state checks is based on actions we have in the current state so far
    in_check_occ = len(curr_actions.check_seqs)
    in_raise_occ = len(curr_actions.raise_seqs)
    in_call_occ = len(curr_actions.call_seqs)    
    in_bet_occ = len(curr_actions.bet_seqs)   
    print "-------------======> in_check_occ:" + str(in_check_occ) + ", in_raise_occ:" + str(in_raise_occ) + ", in_call_occ:" + str(in_call_occ)

    # In-state check:
    if in_check_occ > 0:
      # debug
      print "-------------------========> in_check_occ:" + str(in_check_occ) + " > 0, by opponent: " + str(self.oppo_name)

      # first detect in-state check-raise
      if in_raise_occ > 0:
        # must be a in-state check-raise
        print "-------------------==========> find a in-state check_raise by opponent: " + str(self.oppo_name)
        self.is_in_checkraise = True
      elif in_call_occ > 0:
        # must be a in-state check-call
        print "-------------------==========> find a in-state check_call by opponent: " + str(self.oppo_name)
        self.is_in_checkcall = True 
      else: 
        print "-------------------==========> find NO in-state check_raise or check_call by opponent: " + str(self.oppo_name)
    elif in_bet_occ > 0:
      # debug
      print "-------------------========> in_bet_occ:" + str(in_bet_occ) + " > 0, by opponent: " + str(self.oppo_name)

      # first detect in-state bet-raise
      if in_raise_occ > 0:
        # must be a in-state bet-raise
        print "-------------------==========> find a in-state bet_raise by opponent: " + str(self.oppo_name)
        self.is_in_betraise = True
        # elif in_call_occ > 0:
        #     # must be a in-state bet-call
        #     print "-------------------==========> find a in-state bet_call by opponent: " + str(self.oppo_name)
        #     is_in_betcall = True 
      else: 
        print "-------------------==========> find NO in-state bet_raise or bet_call by opponent: " + str(self.oppo_name)
    else:
      # debug
      print "-------------------========>no check and no bet so far, by opponent: " + str(self.oppo_name)

    # Cross-state check:
    if in_raise_occ > 0 or in_bet_occ > 0:
      # debug
      print "---------------====> has raised in current state by opponent: " + str(self.oppo_name)

      # if the opponent is raising in this state 
      if self.total_check_num_prev == 0:
        # debug
        print "-------------------====>no checks by opponent in previous states: " + str(self.oppo_name)

        # if the opponent never checked but raised/betted 
        if self.total_raise_num_prev > 0 or self.total_bet_num_prev > 0:
          if self.total_call_num_prev == 0:
            # debug
            print "-------------------=====>red alert!! opponent had no checks, no call but raised/betted in previous state: " + str(self.oppo_name)
            # The nighmare - opponent has only raised/bet - no check, no call, most likely have some good hand
            self.is_cross_nocheck_nocall_hasraisebet_raisebet = True
          else: 
            # debug
            print "-------------------=====>no checks, but raised/betted in previous state: " + str(self.oppo_name)
            self.is_cross_nocheck_hascall_hasraisebet_raisebet = True
        else:
          # debug
          print "-------------------=====>no checks, no raised/betted in previous state: " + str(self.oppo_name)
          self.is_cross_nocheck_noraisebet_raisebet = True
      # if opponent raised or bet in this state
      else:
        # debug
        print "-------------------====>has checks by opponent in previous states:" + str(self.oppo_name)

        # if opponent has checked before, there is a cross state check-raise/bet
        self.is_cross_check_raisebet = True

        if self.total_raise_num_prev == 0 and self.total_bet_num_prev == 0:
          # debug
          print "-------------------=====>has checks, but not raised/betted in previous stages : " + str(self.oppo_name)    
          # if opponent never raised before
          self.is_cross_hascheck_noraisebet_raisebet = True

    print "-------------======> oppo eval result boolean starts: <======------------- "
    print "is_large_betraise:" + str(self.is_large_betraise)  
    print "is_small_betraise:" + str(self.is_small_betraise)    
    print "is_in_checkraise:" + str(self.is_in_checkraise)   
    print "is_in_checkcall:" + str(self.is_in_checkcall)
    print "is_in_betraise:" + str(self.is_in_betraise)
    print "is_in_betcall:" + str(self.is_in_betcall)

    print "is_cross_check_raisebet:" + str(self.is_cross_check_raisebet)

    print "is_cross_nocheck_nocall_hasraisebet_raisebet:" + str(self.is_cross_nocheck_nocall_hasraisebet_raisebet)
    print "is_cross_nocheck_hascall_hasraisebet_raisebet:" + str(self.is_cross_nocheck_hascall_hasraisebet_raisebet)
    print "is_cross_nocheck_noraisebet_raisebet:" + str(self.is_cross_nocheck_noraisebet_raisebet)
    print "is_cross_hascheck_noraisebet_raisebet:" + str(self.is_cross_hascheck_noraisebet_raisebet)
    print "-------------======> oppo eval result boolean ends: <======------------- " 
    
    # TODOS: use multiply here instead
    if self.is_cross_nocheck_nocall_hasraisebet_raisebet:
      result += 0.5 * max_opp_eval_limit

    if self.is_cross_nocheck_hascall_hasraisebet_raisebet:
      result += 0.3 * max_opp_eval_limit

    if self.is_large_betraise:
      result += 0.8 * max_opp_eval_limit

    if self.is_in_betraise:
      result += 0.3 * max_opp_eval_limit

    if self.is_cross_check_raisebet:
      result += 0.3 * max_opp_eval_limit

    if self.is_in_checkraise:
      result += 0.3 * max_opp_eval_limit

    print "-------------======> oppo eval calculated result :" + str(result)    

    if result > max_opp_eval_limit:
      result = max_opp_eval_limit
    elif result < min_opp_eval_limit:
      result = min_opp_eval_limit

    print "-------------======> oppo eval actual result :" + str(result)    

    return result
