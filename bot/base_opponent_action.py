class BaseOpponentAction(object):
	def __init__(self,oppo_name,action_state):
		self.oppo_name = oppo_name
		self.phase=action_state
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

	def Action_update(self,action_list):# action_list is 
		if action_list[0] == 'POST':
			self.post_seqs.append(self.action_count)
			self.post_amounts.append(int(action_list[1]))
		elif action_list[0] == 'CALL':
			self.call_seqs.append(self.action_count)
			self.call_amounts.append(int(action_list[1]))
		elif action_list[0] == 'RAISE':
			self.raise_seqs.append(self.action_count)
			self.raise_amounts.append(int(action_list[1]))
		elif action_list[0] == 'BET':
			self.bet_seqs.append(self.action_count)
			self.bet_amounts.append(int(action_list[1]))
		elif action_list[0] == 'CHECK':
			self.check_seqs.append(self.action_count)
		elif action_list[0] == 'FOLD':
			self.fold_seqs.append(self.action_count)
		else:
			print "ACTION TYPE ERROR in BaseOpponentAction"

		self.action_count +=1

