from lib.evaluator import evaluator
import csv
import os

def get_card_equities(row):
	hole_cards = row[row.index('[')+1:-2];
	hole_cards=''.join(hole_cards.split(' '))
	board_card_str = ""
	card_str_2=hole_cards+':xx'
	equity_2 = evaluator.evaluate(card_str_2, board_card_str, '', 1000)
	card_str_3=hole_cards+':xx:xx'
	equity_3 = evaluator.evaluate(card_str_3, board_card_str, '', 1000)
	return [hole_cards,equity_2,equity_3]

def gen_result_keys():
	result_keys = ['game_index','hand_index']
	for tempname in ['dealer','SB','BB']:
		result_keys.append(tempname + '_name');
		result_keys.append(tempname + '_stack');
		result_keys.append(tempname + '_hole_cards');
		result_keys.append(tempname + '_equity_2');
		result_keys.append(tempname + '_equity_3');
		result_keys.append('is_'+tempname + '_enter_preflop');
		result_keys.append(tempname+'_actions_preflop');
		result_keys.append(tempname+'_put2pot_preflop');
	result_keys.append('PreFlop_potsize');
	result_keys.append('flopCards');
	for r in ['flop','turn','river']:
		result_keys.append(r+'Cards')
		for tempname in ['dealer','SB','BB']:
			result_keys.append(tempname+'_equity_2_'+r);
			result_keys.append(tempname + '_equity_3_'+r);
			result_keys.append('is_'+tempname + '_enter_'+r);
			result_keys.append(tempname+'_actions_'+r);
			result_keys.append(tempname+'_put2pot_'+r);
		result_keys.append(r+'_potsize');
	result_keys.pop();
	result_keys.append('final_potsize');
	result_keys.append('is_showdown');
	for tempname in ['dealer','SB','BB']:
		result_keys.append('is_showdown_'+tempname)
		result_keys.append('is_'+tempname+'_win')
	return result_keys

def main():

	LOGPATH_pref = "//home//rongsha//logs//Day_4//Casino_Day-4_Nuts_p"
	OUT_FILENAME = LOGPATH_pref + '.csv'
	OUT_FILE_TEAMS = LOGPATH_pref + '_teams.csv'
	resultmat = []
	teamsmat = []
	result_keys = gen_result_keys()
	headerflag = 0;
	count = 0;
	# for game_index in [1]:
	for game_index in range(1,7):
		LOGPATH = LOGPATH_pref+str(game_index) + '//'
		for MATCHNAME in os.listdir(LOGPATH):
			# OUT_FILENAME = LOGPATH + MATCHNAME + '.csv'

			
			print (LOGPATH+MATCHNAME)
			with open(LOGPATH+MATCHNAME, 'r') as f:
				for row in f.readlines():
					
					if count > 1000:
						f = open(OUT_FILENAME,'a')
						dict_writer = csv.DictWriter(f,fieldnames=result_keys)
						print result_keys;
						if headerflag == 0: 
							dict_writer.writeheader()
						dict_writer.writerows(resultmat)
						f.close()
						resultmat = [];
						count = 0;
						headerflag = 1;
					if '6.176 MIT Pokerbots' in row:
						continue;
					elif row[0:4]=="Hand": # a new hand
						count += 1
						state = 'preflop'
						temp_strs = row.split(', ');
						hand_index = int(temp_strs[0].strip('Hand #'))

						dealer_info = temp_strs[1].split(' ')
						dealer_name = dealer_info[0];
						dealer_stack = dealer_info[1].strip('()')
						SB_info = temp_strs[2].split(' ')
						SB_name = SB_info[0];
						SB_stack = SB_info[1].strip('()')
						BB_info = temp_strs[3].split(' ')
						BB_name = BB_info[0];
						BB_stack = BB_info[1].strip('()\n')

						names = {}
						names[dealer_name] = 'dealer';
						names[SB_name] = 'SB'
						names[BB_name] = 'BB'


						result = {}
						result['game_index'] = game_index;
						result['hand_index'] = hand_index;
						result['dealer_name'] = dealer_name;
						result['dealer_stack'] = dealer_stack;
						result['SB_name'] = SB_name;
						result['SB_stack'] = SB_stack;
						result['BB_name'] = BB_name;
						result['BB_stack'] = BB_stack;
						# initialization
						result['PreFlop_potsize'] = 'null'
						result['flopCards'] = 'null'
						result['flop_potsize'] = 'null'
						result['turnCards'] = 'null'
						result['turn_potsize'] = 'null'
						result['riverCards'] = 'null'

						result['is_showdown'] = False
						result['is_showdown_dealer'] = False
						result['is_showdown_SB'] = False
						result['is_showdown_BB'] = False
						result['is_dealer_win'] = False
						result['is_SB_win'] = False
						result['is_BB_win'] = False
						result['final_potsize'] = 0

						for tempname in ['dealer','SB','BB']:
							for tempstate in ['flop','turn','river']:
								tempstr = 'is_'+tempname+'_enter_' + tempstate
								result[tempstr] = False
								for k in ['2','3'] :
									tempstr = tempname + '_equity_'+k+'_' + tempstate
									result[tempstr] = 'null';
							

						for tempname in ['dealer','SB','BB']:
							for tempstate in ['preflop','flop','turn','river']:
								result[tempname + '_actions_' + tempstate] = '';
								result[tempname + '_put2pot_' + tempstate] = 0;




					elif 'Dealt' in row:
						board_card_str='';
						curname = row.split(' ')[2];
						hole_info = get_card_equities(row);
						result[names[curname]+'_hole_cards'] = hole_info[0];
						result[names[curname]+'_equity_2'] = hole_info[1];
						result[names[curname]+'_equity_3'] = hole_info[2];
						# if dealer_name in row:
						# 	hole_info = get_card_equities(row)
						# 	result['dealer_hole_cards'] = hole_info[0];
						# 	result['dealer_equity_2'] = hole_info[1];
						# 	result['dealer_equity_3'] = hole_info[2];

						# elif SB_name in row:
						# 	hole_info = get_card_equities(row)
						# 	result['SB_hole_cards'] = hole_info[0];
						# 	result['SB_equity_2'] = hole_info[1];
						# 	result['SB_equity_3'] = hole_info[2];
						# elif BB_name in row:
						# 	hole_info = get_card_equities(row)
						# 	result['BB_hole_cards'] = hole_info[0];
						# 	result['BB_equity_2'] = hole_info[1];
						# 	result['BB_equity_3'] = hole_info[2];


					elif '*** FLOP ***' in row:
						state = 'flop'
						result['PreFlop_potsize'] = row[row.index('(')+1:row.index(')')];
						result['flopCards'] = ''.join(row[row.index('[')+1:row.index(']')].split(' '))
						board_card_str = result['flopCards']
						for tempname in ['dealer','SB','BB']:
							result[tempname+'_equity_2_flop'] = evaluator.evaluate(result[tempname+'_hole_cards']+':xx', board_card_str, '', 1000)
							result[tempname+'_equity_3_flop'] = evaluator.evaluate(result[tempname+'_hole_cards']+':xx:xx', board_card_str, '', 1000)

						# result['dealer_equity_2_flop'] = evaluator.evaluate(result['dealer_hole_cards']+':xx', board_card_str, '', 1000)
						# result['dealer_equity_3_flop'] = evaluator.evaluate(result['dealer_hole_cards']+':xx:xx', board_card_str, '', 1000)
						# result['SB_equity_2_flop'] = evaluator.evaluate(result['SB_hole_cards']+':xx', board_card_str, '', 1000)
						# result['SB_equity_3_flop'] = evaluator.evaluate(result['SB_hole_cards']+':xx:xx', board_card_str, '', 1000)
						# result['BB_equity_2_flop'] = evaluator.evaluate(result['BB_hole_cards']+':xx', board_card_str, '', 1000)
						# result['BB_equity_3_flop'] = evaluator.evaluate(result['BB_hole_cards']+':xx:xx', board_card_str, '', 1000)
					elif '*** TURN ***'	in row:
						state = 'turn'
						result['flop_potsize'] = row[row.index('(')+1:row.index(')')];
						temp_turnCards = row[row.find('[')+1:row.find(']')] + row[row.rfind('[')+1:row.rfind(']')]
						result['turnCards'] = ''.join(temp_turnCards.split(' '))
						board_card_str = result['turnCards']
						for tempname in ['dealer','SB','BB']:
							result[tempname+'_equity_2_turn'] = evaluator.evaluate(result[tempname+'_hole_cards']+':xx', board_card_str, '', 1000)
							result[tempname+'_equity_3_turn'] = evaluator.evaluate(result[tempname+'_hole_cards']+':xx:xx', board_card_str, '', 1000)
					elif '*** RIVER ***' in row: 
						state = 'river'
						result['turn_potsize'] = row[row.index('(')+1:row.index(')')];
						temp_rivercards = row[row.find('[')+1:row.find(']')] + row[row.rfind('[')+1:row.rfind(']')]
						result['riverCards'] = ''.join(temp_rivercards.split(' '))
						board_card_str = result['riverCards']
						for tempname in ['dealer','SB','BB']:
							result[tempname+'_equity_2_river'] = evaluator.evaluate(result[tempname+'_hole_cards']+':xx', board_card_str, '', 1000)
							result[tempname+'_equity_3_river'] = evaluator.evaluate(result[tempname+'_hole_cards']+':xx:xx', board_card_str, '', 1000)
					elif 'shows' in row:
						result['is_showdown'] = True
						showdown_name = row.split(' ')[0]
						if showdown_name == result['dealer_name']:
							result['is_showdown_dealer'] = True
						elif showdown_name == result['SB_name']:
							result['is_showdown_SB'] = True
						elif showdown_name == result['BB_name']:
							result['is_showdown_BB'] = True
					elif 'wins' in row:
						winner_name = row.split(' ')[0]
						if winner_name == result['dealer_name']:
							result['is_dealer_win'] = True
						elif winner_name == result['SB_name']:
							result['is_SB_win'] = True
						elif winner_name == result['BB_name']:
							result['is_BB_win'] = True
						result['final_potsize'] = int(row[row.index('(')+1:row.index(')')])
					elif 'ties' in row:
						winner_name = row.split(' ')[0]
						if winner_name == result['dealer_name']:
							result['is_dealer_win'] = True
						elif winner_name == result['SB_name']:
							result['is_SB_win'] = True
						elif winner_name == result['BB_name']:
							result['is_BB_win'] = True				
						result['final_potsize'] += int(row[row.index('(')+1:row.index(')')])
					elif row == '\n':
						resultmat.append(result)
					elif (row.split(' ')[0] in [dealer_name,SB_name,BB_name]) and ('posts' not in row): # actions:
						curname = row.split(' ')[0];
						result['is_'+names[curname]+'_enter_'+state] = True
						tempstr2 = names[curname]+'_actions_'+state
						if row.split(' ')[1] == 'checkes':
							result[tempstr2] += 'H';
						elif row.split(' ')[1] in ['bets','raises']:
							result[tempstr2] += 'R';
							result[names[curname]+'_put2pot_'+state] = row.split(' ')[-1].strip('\n');
						elif row.split(' ')[1] == 'calls':
							result[tempstr2] += 'A';
							result[names[curname]+'_put2pot_'+state] = row.split(' ')[-1].strip('\n');
						elif row.split(' ')[1] == 'folds':
							result[tempstr2] += 'F';
					elif 'posts' in row:
						curname = row.split(' ')[0];
						result[names[curname]+'_put2pot_'+state] = row.split(' ')[5].strip('\n')
						result['is_'+names[curname]+'_enter_'+state] = True

				# end of each match
				tempdict = {};
				teamsresult={}
				for tempname in ['dealer','SB','BB']:
					tempdict[result[tempname+'_name']] = result[tempname+'_stack'];
				rankings = sorted(tempdict,key=tempdict.get,reverse=True);
				rankings_other = filter(lambda x:x!='Nuts',rankings)
				teamsresult['win']=rankings_other[0];
				teamsresult['loss'] = rankings_other[1];
				teamsmat.append(teamsresult);



			



	f2 = open(OUT_FILE_TEAMS,'w')
	dict_writer2 = csv.DictWriter(f2,fieldnames=['win','loss'])
	dict_writer2.writeheader()
	dict_writer2.writerows(teamsmat)




if __name__ == "__main__":
    main()



