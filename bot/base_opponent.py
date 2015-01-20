import base_opponent_action

class BaseOpponent(object):
	def __init__(self,name,player):
		self.player = player
		self.oppo_name = name;
		self.is_active_in_game = True
		self.is_active_in_hand = True
		self.stack_size_new_hand = 0

		self.reset()

	def reset(self):
		#debug
		print "-------======> enter base_opponent.reset()"

		self.is_active_in_hand = True

		self.all_actions = [];
		self.last_state = ''

		# total stats
		self.total_check_num = 0

		self.total_call_num = 0
		self.total_call_amount = 0

		self.total_raise_num = 0
		self.total_raise_amount = 0

		self.total_bet_num = 0
		self.total_bet_amount = 0		

		# total stats in previous states
		self.total_check_num_prev = 0

		self.total_call_num_prev = 0
		self.total_call_amount_prev = 0

		self.total_raise_num_prev = 0
		self.total_raise_amount_prev = 0

		self.total_bet_num_prev = 0
		self.total_bet_amount_prev = 0		

	def update_prev_states_stats(self):
		self.total_check_num_prev = self.total_check_num

		self.total_call_num_prev = self.total_call_num
		self.total_call_amount_prev = self.total_call_amount

		self.total_raise_num_prev = self.total_raise_num
		self.total_raise_amount_prev = self.total_raise_amount

		self.total_bet_num_prev = self.total_bet_num
		self.total_bet_amount_prev = self.total_bet_amount	

	def Oppo_update(self,action_state,one_action):
		#debug
		print "-------====!!==> enter Oppo_update(), oppo_name: " + self.oppo_name + ", action_state: " + str(action_state) + ", one_action: " + str(one_action) + ", is_active_in_hand:" + str(self.is_active_in_hand)

		if self.last_state == '':
			#debug
			print "-------====!!==> Oppo_update(), enter if{} (when opponent is intialized), action_state: " + str(action_state) + ", all_actions:" + str(self.all_actions) + ", one_action: " + str(one_action)

			# initial state when opponent is intialized
			new_action=base_opponent_action.BaseOpponentAction(self.oppo_name,action_state, self)
			new_action.Action_update(one_action)
			self.all_actions.append(new_action)
			self.last_state = action_state;

			#debug
			print "-------====!!==> Oppo_update(), exit if{}... (when opponent is intialized), action_state: " + str(action_state) + "all_actions count:" + str(len(self.all_actions)) + ", one_action: " + str(one_action)

		elif (action_state == self.last_state):
			#debug
			print "-------====!!==> Oppo_update(), enter elif{} (when still in the same state), action_state: " + str(action_state) + ", all_actions count:" + str(len(self.all_actions)) + ", one_action: " + str(one_action)

			self.all_actions[-1].Action_update(one_action)
			#debug
			print "-------====!!==> Oppo_update(), exit elif{}... (when still in the same state), action_state: " + str(action_state) + ", all_actions count:" + str(len(self.all_actions)) + ", one_action: " + str(one_action)

		else:
			#debug
			print "-------====!!==> Oppo_update(), enter else{} (when switch to a new state), action_state: " + str(action_state) + ", all_actions count:" + str(len(self.all_actions)) + ", one_action: " + str(one_action)

			# when switch to a new state
			new_action=base_opponent_action.BaseOpponentAction(self.oppo_name,action_state, self)
			new_action.Action_update(one_action)
			self.all_actions.append(new_action)
			self.last_state = action_state
			self.update_prev_states_stats()
			#debug
			print "-------====!!==> Oppo_update(), exit else{}... (when switch to a new state), action_state: " + str(action_state) + ", all_actions count:" + str(len(self.all_actions)) + ", one_action: " + str(one_action)

		#debug
		print "-------====!!==> exiting Oppo_update()..., oppo_name: " + self.oppo_name + ", action_state: " + str(action_state) + ", all_actions count:" + str(len(self.all_actions)) + ", one_action: " + str(one_action) + ", is_active_in_hand:" + str(self.is_active_in_hand)			
