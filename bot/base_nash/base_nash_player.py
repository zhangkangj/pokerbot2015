from .. import base_player
#import base_nash_bot

from bot.mixed import mixed_bot

#import mixedoppnew_opponent

import base_nash_bot


class Base_nashPlayer(base_player.BasePlayer):
  def __init__(self):
    super(Base_nashPlayer, self).__init__()
    self.current_bot = mixed_bot.MixedBot(self) ## by defalt it uses mixed
    self.nash_bot1 = base_nash_bot.Base_nashBot(self, 300, '../../data/cfr/aws/prob_300_total.npy')
    self.current_bot_type = 'MIXED'


  def new_game(self, parts):
    print 'fdsafsdafsdafsda call new game bash nash'
    super(Base_nashPlayer, self).new_game(parts)
    
    
  def new_hand(self, parts):
    super(Base_nashPlayer, self).new_hand(parts);
    if self.num_active_player == 2 and (self.current_bot_type != 'NASH'):
    	self.current_bot = self.nash_bot1
    	#self.current_bot = base_nash_bot.Base_nashBot(self, 100, ' ')
    	self.current_bot_type = 'NASH'
    	print 'Now change to nash bot for new hand'
    elif self.num_active_player == 3 and (self.current_bot_type != 'MIXED'):
    	self.current_bot = mixed_bot.MixedBot(self)
    	self.current_bot_type = 'MIXED'
    	print 'Now change to mixed bot for new hand'
    else:
    	print 'Current player:' + self.current_bot_type
    
  def handover(self, parts):
    super(Base_nashPlayer, self).handover(parts)


  def prepare_last_actions(self,active_name,inactive_name,last_acts):
    modified_acts = [];
    modstate=0
    for act in last_acts:
      if (act[0] != inactive_name) and (modstate == 0):
        modified_acts.append(act);
      elif (act[0] == active_name) and (modstate == 1):
        modstate = 0;
        newtup = (act[0],'RAISE',act[-1])
        modified_acts.append(newtup)
      elif (act[0] == self.player_name) and (modstate == 1):
        modstate = 0;
        newtup = (act[0],'RAISE',act[-1]);
        modified_acts.append(newtup)
      elif act[0] == inactive_name:
        if ('RAISE' not in act[1]) and ('BET' not in act[1]):
          pass
        else:
          if len(modified_acts) == 0:
            modstate = 1;
          else:
            lastelm = modified_acts.pop()
            if lastelm[0] == active_name:
              newtup = (lastelm[0],'RAISE',act[-1])
              modified_acts.append(newtup)
            else:
              modstate = 1
              modified_acts.append(lastelm)
      else:
        print 'ERROR in mapping 3->2 in base_nash_player'
    return modified_acts

  def further_process_init(self,last_actions_xxx_init):
    # cannot end with two calls
    if len(last_actions_xxx_init) > 2 and last_actions_xxx_init[-1][1] == 'CALL' and last_actions_xxx_init[-2][1] == 'CALL':
      last_actions_xxx_init.pop()
    # call/check cannot before raise/bet
    if len(last_actions_xxx_init) > 2:
      raiseflag = 0;
      for i in range(-1,-len(last_actions_xxx_init)-1,-1):
        if last_actions_xxx_init[i][1] in ['RAISE','BET']:
          raiseflag = 1;
        elif raiseflag == 1 and last_actions_xxx_init[i][1] in ['CALL','CHECK']:
          newtup = (last_actions_xxx_init[i][0],'RAISE',max(0,last_actions_xxx_init[i][2])+1);
          last_actions_xxx_init[i] = newtup;
          raiseflag = 0;
    return last_actions_xxx_init

  def action(self,parts):
    super(Base_nashPlayer, self).action(parts);
    if self.num_active_player_dynamic == 2 and self.action_state != 'PREFLOP' and (self.current_bot_type != 'NASH'):
      print 'Now change to nash bot for new action'
      print 'self.last_actions_preflop:'+str(self.last_actions_preflop);
      print 'self.last_actions_flop:', self.last_actions_flop;  
      print 'self.last_actions_turn:', self.last_actions_turn;
      print 'self.last_actions_river:', self.last_actions_river;
      self.last_actions_preflop_init = self.prepare_last_actions(self.active_name,self.inactive_name,self.last_actions_preflop)
      self.last_actions_flop_init = self.prepare_last_actions(self.active_name,self.inactive_name,self.last_actions_flop)
      self.last_actions_turn_init = self.prepare_last_actions(self.active_name,self.inactive_name,self.last_actions_turn)
      self.last_actions_river_init = self.prepare_last_actions(self.active_name,self.inactive_name,self.last_actions_river)
      print 'last_actions_preflop_init:::' + str(self.last_actions_preflop_init)
      print 'last_actions_flop_init:::' + str(self.last_actions_flop_init)
      print 'last_actions_turn_init:::' + str(self.last_actions_turn_init)
      print 'last_actions_river_init:::' + str(self.last_actions_river_init)

      # if I am SB: I post 1, oppo1 posts2, oppo2 called/fold.
      if self.last_actions_preflop[0][0] == self.player_name and self.last_actions_preflop[2][1] in ['CALL','FOLD']:
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [(self.player_name,'POST',1),(self.active_name,'POST',2)]+self.last_actions_preflop_init
        # if used to conclude by check and now conclude by me: should conclude by him
        if self.last_actions_preflop_init[-1][0] == self.player_name and self.last_actions_preflop[-1][1] == 'CHECK':
          self.last_actions_preflop_init = self.last_actions_preflop_init + [(self.active_name,'CHECK',None)]
      # if I am SB: I post 1, oppo1 posts 2, oppo2 raised. then suppose I called and oppo raised
      elif self.last_actions_preflop[0][0] == self.player_name and self.last_actions_preflop_init[1][1] == 'RAISE':
        firstelm = self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [firstelm , (self.active_name,'POST',2) , (self.player_name,'CALL',2)] + self.last_actions_preflop_init
        # if I am BB and SB fold. I change to SB.I post1, oppo post 2, i called. then whatever.
      elif self.last_actions_preflop[1][0] == self.player_name and self.last_actions_preflop_init[0][0] == self.player_name and self.last_actions_preflop_init[0][1] == 'CALL':
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [(self.player_name,'POST',1),(self.active_name,'POST',2),(self.player_name,'CALL',2)] + self.last_actions_preflop_init
        # if last one is check. was conclued by me. should concluded by him.
        if self.last_actions_preflop[-1][1] == 'CHECK':
          self.last_actions_preflop_init.pop()
          self.last_actions_preflop_init.pop()
          self.last_actions_preflop_init = self.last_actions_preflop_init + [(self.active_name,'CHECK',None)]
       # if I am BB and SB fold, and I raised. I change to SB. i post 1, BB post 2, I raise
      elif self.last_actions_preflop[1][0] == self.player_name and self.last_actions_preflop_init[0][0] == self.player_name and self.last_actions_preflop_init[0][1] == 'RAISE': 
        self.last_actions_preflop_init.pop()
        self.last_actions_preflop_init.pop()
        self.last_actions_preflop_init = [(self.player_name,'POST',1),(self.active_name,'POST',2)] + self.last_actions_preflop_init
        # if I am BB and dealer fold. nothing changed.
      elif self.last_actions_preflop[1][0] == self.player_name and self.last_actions_preflop_init[1][0] == self.player_name:
        pass
      # if I am dealer and i called. then I am BB and start from SB.
      elif self.last_actions_preflop[2][0] == self.player_name and self.last_actions_preflop[2][1] == 'CALL':
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [(self.active_name,'POST',1) , (self.player_name,'POST',2)]+self.last_actions_preflop_init
        # I have to conclude the round. if last one is check. then oppo call and I check.
        if self.last_actions_preflop[-1][1] == 'CHECK':
          self.last_actions_preflop_init.pop()
          self.last_actions_preflop_init = self.last_actions_preflop_init + [(self.active_name,'CALL',2),(self.player_name,'CHECK',None)]
          # if I am dealer and I raised. Then I am BB and SB called, and I raised
      elif self.last_actions_preflop[2][0] == self.player_name and self.last_actions_preflop[2][1] == 'RAISE':            
        self.last_actions_preflop_init.pop(0)
        self.last_actions_preflop_init = [(self.active_name,'POST',1) , (self.player_name,'POST',2) , (self.active_name,'CALL',2)]+self.last_actions_preflop_init
      else:
        print "Should be legal..."
        # delete redundant calls

      self.last_actions_preflop_init = self.further_process_init(self.last_actions_preflop_init)
      self.last_actions_flop_init = self.further_process_init(self.last_actions_flop_init)
      self.last_actions_turn_init = self.further_process_init(self.last_actions_turn_init)
      self.last_actions_river_init = self.further_process_init(self.last_actions_river_init)

      action_seq = self.last_actions_preflop_init      
      if self.num_board_card >= 3:
        action_seq = action_seq + [('FLOP', 'DEAL', None)] + self.last_actions_flop_init
      if self.num_board_card >= 4:
        action_seq = action_seq + [('TURN', 'DEAL', None)] + self.last_actions_turn_init
      if self.num_board_card >= 5:
        action_seq = action_seq + [('RIVER', 'DEAL', None)] + self.last_actions_river_init       

      print 'last_actions_preflop_init:::' + str(self.last_actions_preflop_init)
      print 'last_actions_flop_init:::' + str(self.last_actions_flop_init)
      print 'last_actions_turn_init:::' + str(self.last_actions_turn_init)
      print 'last_actions_river_init:::' + str(self.last_actions_river_init)

      # if max(len(self.last_actions_preflop_init),len(self.last_actions_flop_init),len(self.last_actions_turn_init),len(self.last_actions_river_init)) < 7:
      #   # max < 7 then can change bot
      

      if self.nash_bot1.initialize_from_beginning(action_seq):
        self.current_bot = self.nash_bot1
        self.current_bot_type = 'NASH'
      

    	###############!!!!!!!!!!!!!!!!!!!!!!!!!##################
    	#### INIT bot based on last_actions_init lists!!########
    	##
    	##
    	##
    	##
		
