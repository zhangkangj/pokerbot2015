from lib.evaluator import evaluator


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
	LOGPATH = "log//test//"
	MATCHNAME = "match_P1_P2_P3_01_12_00_50_37_9332.txt"

	match_index = 1
	game_index = 1
	resultmat = []
	with open(LOGPATH+MATCHNAME, 'r') as f:
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
				BB_stack = BB_info[1].strip('()')
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
			elif row == '\n':
				resultmat.append(result)





if __name__ == "__main__":
    main()



