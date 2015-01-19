import base_opponent_action
class BaseOpponent(object):
	def __init__(self,name):
		self.oppo_name = name;
		self.all_actions = [];
		self.last_state = ''

	def Oppo_update(self,action_state,action_list):
		if self.last_state == '':
			new_action=base_opponent_action.BaseOpponentAction(self.oppo_name,action_state)
			new_action.Action_update(action_list);
			self.all_actions.append(new_action);
			self.last_state = action_state;
		elif (action_state == self.last_state):
			self.all_actions[-1].Action_update(action_list)
		else:
			new_action=base_opponent_action.BaseOpponentAction(self.oppo_name,action_state)
			new_action.Action_update(action_list);
			self.all_actions.append(new_action);
			self.last_state = action_state;

