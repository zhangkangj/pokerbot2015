from lib.evaluator import evaluator
import csv

def get_card_equities(row):
	hole_cards = row[row.index('[')+1:-2];
	hole_cards=''.join(hole_cards.split(' '))
	board_card_str = ""
	card_str_2=hole_cards+':xx'
	equity_2 = evaluator.evaluate(card_str_2, board_card_str, '', 1000)
	card_str_3=hole_cards+':xx:xx'
	equity_3 = evaluator.evaluate(card_str_3, board_card_str, '', 1000)
	return [hole_cards,equity_2,equity_3]


def main():
	LOGPATH = "//home//rongsha//logs//Day_2//"
	MATCHNAME = "Casino_Day-2_TheHouse_vs_Titan_vs_Nuts"
	OUT_FILENAME = LOGPATH + MATCHNAME + '.csv'

	match_index = 1
	game_index = 1
	resultmat = []
	count = 0
	with open(LOGPATH+MATCHNAME+'.txt', 'r') as f:
		for row in f.readlines():
			if row[0:4]=="Hand": # a new hand
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
				result = {}
				result['match_index'] = match_index;
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
				result['FlopCards'] = 'null'
				result['dealer_equity_2_flop'] = 'null'
				result['dealer_equity_3_flop'] = 'null'
				result['SB_equity_2_flop'] = 'null'
				result['SB_equity_3_flop'] = 'null'
				result['BB_equity_2_flop'] = 'null'
				result['BB_equity_3_flop'] = 'null'
				result['Flop_potsize'] = 'null'
				result['TurnCards'] = 'null'
				result['dealer_equity_2_turn'] = 'null'
				result['dealer_equity_3_turn'] = 'null'
				result['SB_equity_2_turn'] = 'null'
				result['SB_equity_3_turn'] = 'null'
				result['BB_equity_2_turn'] = 'null'
				result['BB_equity_3_turn'] = 'null'
				result['Turn_potsize'] = 'null'
				result['RiverCards'] = 'null'
				result['dealer_equity_2_river'] = 'null'
				result['dealer_equity_3_river'] = 'null'
				result['SB_equity_2_river'] = 'null'
				result['SB_equity_3_river'] = 'null'
				result['BB_equity_2_river'] = 'null'
				result['BB_equity_3_river'] = 'null'

				result['is_showdown'] = False
				result['is_showdown_dealer'] = False
				result['is_showdown_SB'] = False
				result['is_showdown_BB'] = False
				result['is_dealer_win'] = False
				result['is_SB_win'] = False
				result['is_BB_win'] = False
				result['final_potsize'] = 0

			elif 'Dealt' in row:
				board_card_str='';
				if dealer_name in row:
					hole_info = get_card_equities(row)
					result['dealer_hole_cards'] = hole_info[0];
					result['dealer_equity_2'] = hole_info[1];
					result['dealer_equity_3'] = hole_info[2];

				elif SB_name in row:
					hole_info = get_card_equities(row)
					result['SB_hole_cards'] = hole_info[0];
					result['SB_equity_2'] = hole_info[1];
					result['SB_equity_3'] = hole_info[2];
				elif BB_name in row:
					hole_info = get_card_equities(row)
					result['BB_hole_cards'] = hole_info[0];
					result['BB_equity_2'] = hole_info[1];
					result['BB_equity_3'] = hole_info[2];


			elif '*** FLOP ***' in row:
				result['PreFlop_potsize'] = row[row.index('(')+1:row.index(')')];
				result['FlopCards'] = ''.join(row[row.index('[')+1:row.index(']')].split(' '))
				board_card_str = result['FlopCards']
				result['dealer_equity_2_flop'] = evaluator.evaluate(result['dealer_hole_cards']+':xx', board_card_str, '', 1000)
				result['dealer_equity_3_flop'] = evaluator.evaluate(result['dealer_hole_cards']+':xx:xx', board_card_str, '', 1000)
				result['SB_equity_2_flop'] = evaluator.evaluate(result['SB_hole_cards']+':xx', board_card_str, '', 1000)
				result['SB_equity_3_flop'] = evaluator.evaluate(result['SB_hole_cards']+':xx:xx', board_card_str, '', 1000)
				result['BB_equity_2_flop'] = evaluator.evaluate(result['BB_hole_cards']+':xx', board_card_str, '', 1000)
				result['BB_equity_3_flop'] = evaluator.evaluate(result['BB_hole_cards']+':xx:xx', board_card_str, '', 1000)
			elif '*** TURN ***'	in row:
				result['Flop_potsize'] = row[row.index('(')+1:row.index(')')];
				temp_turncards = row[row.find('[')+1:row.find(']')] + row[row.rfind('[')+1:row.rfind(']')]
				result['TurnCards'] = ''.join(temp_turncards.split(' '))
				board_card_str = result['TurnCards']
				result['dealer_equity_2_turn'] = evaluator.evaluate(result['dealer_hole_cards']+':xx', board_card_str, '', 1000)
				result['dealer_equity_3_turn'] = evaluator.evaluate(result['dealer_hole_cards']+':xx:xx', board_card_str, '', 1000)
				result['SB_equity_2_turn'] = evaluator.evaluate(result['SB_hole_cards']+':xx', board_card_str, '', 1000)
				result['SB_equity_3_turn'] = evaluator.evaluate(result['SB_hole_cards']+':xx:xx', board_card_str, '', 1000)
				result['BB_equity_2_turn'] = evaluator.evaluate(result['BB_hole_cards']+':xx', board_card_str, '', 1000)
				result['BB_equity_3_turn'] = evaluator.evaluate(result['BB_hole_cards']+':xx:xx', board_card_str, '', 1000)
			elif '*** RIVER ***' in row: 
				result['Turn_potsize'] = row[row.index('(')+1:row.index(')')];
				temp_rivercards = row[row.find('[')+1:row.find(']')] + row[row.rfind('[')+1:row.rfind(']')]
				result['RiverCards'] = ''.join(temp_rivercards.split(' '))
				board_card_str = result['RiverCards']
				result['dealer_equity_2_river'] = evaluator.evaluate(result['dealer_hole_cards']+':xx', board_card_str, '', 1000)
				result['dealer_equity_3_river'] = evaluator.evaluate(result['dealer_hole_cards']+':xx:xx', board_card_str, '', 1000)
				result['SB_equity_2_river'] = evaluator.evaluate(result['SB_hole_cards']+':xx', board_card_str, '', 1000)
				result['SB_equity_3_river'] = evaluator.evaluate(result['SB_hole_cards']+':xx:xx', board_card_str, '', 1000)
				result['BB_equity_2_river'] = evaluator.evaluate(result['BB_hole_cards']+':xx', board_card_str, '', 1000)
				result['BB_equity_3_river'] = evaluator.evaluate(result['BB_hole_cards']+':xx:xx', board_card_str, '', 1000)
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

	
	result_keys = ['match_index','game_index','hand_index','dealer_name','SB_name','BB_name','dealer_stack','SB_stack','BB_stack','dealer_hole_cards','dealer_equity_2','dealer_equity_3','SB_hole_cards','SB_equity_2','SB_equity_3','BB_hole_cards','BB_equity_2','BB_equity_3','PreFlop_potsize','FlopCards','dealer_equity_2_flop','dealer_equity_3_flop','SB_equity_2_flop','SB_equity_3_flop','BB_equity_2_flop','BB_equity_3_flop','Flop_potsize','TurnCards','dealer_equity_2_turn','dealer_equity_3_turn','SB_equity_2_turn','SB_equity_3_turn','BB_equity_2_turn','BB_equity_3_turn','Turn_potsize','RiverCards','dealer_equity_2_river','dealer_equity_3_river','SB_equity_2_river','SB_equity_3_river','BB_equity_2_river','BB_equity_3_river','final_potsize','is_showdown','is_showdown_dealer','is_showdown_SB','is_showdown_BB','is_dealer_win','is_SB_win','is_BB_win']
	f = open(OUT_FILENAME,'w')
	dict_writer = csv.DictWriter(f,fieldnames=result_keys)
	dict_writer.writeheader()
	# dict_writer = csv.DictWriter(f,result_keys)
	# dict_writer.writer.writerow(result_keys);
	dict_writer.writerows(resultmat)




if __name__ == "__main__":
    main()



