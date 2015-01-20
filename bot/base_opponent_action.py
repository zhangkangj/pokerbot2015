class BaseOpponentAction(object):
	def __init__(self,oppo_name,action_state,opponent):
		self.oppo_name = oppo_name
		self.state=action_state
		self.call_seqs=[];
		self.call_amounts=[];
		self.raise_seqs=[]
		self.raise_amounts=[]
		self.bet_seqs=[]
		self.bet_amounts=[]
		self.post_seqs=[]
		self.post_amounts=[]
		self.check_seqs=[]
		self.fold_seqs=[]
		self.action_count = 0
		self.opponent = opponent

	def Action_update(self,action_list):# action_list is
		print "-----------##====> enter Action_update(): self.opponent.oppo_name:" + self.opponent.oppo_name + ", action_list:" + str(action_list) 

		if action_list[0] == 'POST':
			action_amount = int(action_list[1])
			self.post_seqs.append(self.action_count)
			self.post_amounts.append(action_amount)
		elif action_list[0] == 'CALL':
			action_amount = int(action_list[1])
			self.call_seqs.append(self.action_count)
			self.call_amounts.append(action_amount)
			self.opponent.total_call_num += 1
			self.opponent.total_call_amount += action_amount			
		elif action_list[0] == 'RAISE':
			action_amount = int(action_list[1])
			self.raise_seqs.append(self.action_count)
			self.raise_amounts.append(action_amount)
			self.opponent.total_raise_num += 1
			self.opponent.total_raise_amount += action_amount			
		elif action_list[0] == 'BET':
			action_amount = int(action_list[1])
			self.bet_seqs.append(self.action_count)
			self.bet_amounts.append(action_amount)
			self.opponent.total_bet_num += 1
			self.opponent.total_bet_amount += action_amount		
		elif action_list[0] == 'CHECK':
			self.check_seqs.append(self.action_count)
			self.opponent.total_check_num += 1
		elif action_list[0] == 'FOLD':
			self.fold_seqs.append(self.action_count)
			# set the opponent to be inactive
			self.opponent.is_active_in_hand = False
			#debug
			print "-----------##======> self.opponent.oppo_name:" + self.opponent.oppo_name + " folded, set self.opponent.is_active_in_hand:" + str(self.opponent.is_active_in_hand)
		else:
			print "ACTION TYPE ERROR in BaseOpponentAction"

		print "-----------##====> exit Action_update()...: self.opponent.oppo_name:" + self.opponent.oppo_name + ", action_list:" + str(action_list) 

		self.action_count +=1

