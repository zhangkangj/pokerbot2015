import numpy as np
import Gamestat

MAX_BET = 3

def count_game_state(game_state, round,gamestat):
    if round == 'PREFLOP':
        if game_state == 'D':
            gamestat.num_preflop_state += 1
            gamestat.num_preflop_state_D += 1
        elif game_state == 'SB':
            gamestat.num_preflop_state += 1
            gamestat.num_preflop_state_SB += 1
        elif game_state == 'BB':
            gamestat.num_preflop_state += 1
            gamestat.num_preflop_state_BB += 1
    elif round == 'FLOP':
        if game_state == 'D':
            gamestat.num_flop_state += 1
            gamestat.num_flop_state_D += 1
        elif game_state == 'SB':
            gamestat.num_flop_state += 1
            gamestat.num_flop_state_SB += 1
        elif game_state == 'BB':
            gamestat.num_flop_state += 1
            gamestat.num_flop_state_BB += 1
    elif round == 'TURN':
        if game_state == 'D':
            gamestat.num_turn_state += 1
            gamestat.num_turn_state_D += 1
        elif game_state == 'SB':
            gamestat.num_turn_state += 1
            gamestat.num_turn_state_SB += 1
        elif game_state == 'BB':
            gamestat.num_turn_state += 1
            gamestat.num_turn_state_BB += 1
    elif round == 'RIVER':
        if game_state == 'D':
            gamestat.num_river_state += 1
            gamestat.num_river_state_D += 1
        elif game_state == 'SB':
            gamestat.num_river_state += 1
            gamestat.num_river_state_SB += 1
        elif game_state == 'BB':
            gamestat.num_river_state += 1
            gamestat.num_river_state_BB += 1
    if game_state == 'ENDGAME':
        gamestat.num_end_state += 1

def get_winners():
    return (0,0,1)

        
def get_legal_actions(stacks, pot_sizes, bet_in_round, active_player):
    if active_player == 'D':
        index = 0
    elif active_player == 'SB':
        index = 1
    elif active_player == 'BB':
        index = 2
    else:
        return [' ']

    if pot_sizes[index] == np.max(pot_sizes):
        pot = np.sum(pot_sizes)
        if stacks[index] < 2 or bet_in_round == MAX_BET:
            return ['CHECK']
        elif stacks[index] <pot/2:
            return ['CHECK','BET:2']
        elif stacks[index] <pot:
            return ['CHECK','BET:2','BET:'+str(pot/2)]
        else:
            return ['CHECK','BET:2','BET:'+str(pot/2),'BET:'+str(pot)]
    else:
        call_amount = np.max(pot_sizes) - pot_sizes[index]
        pot = np.sum(pot_sizes) + call_amount
        if call_amount >= stacks[index]:
            return ['FOLD','CALL:'+str(stacks[index])]
        elif stacks[index] - call_amount < 2 or bet_in_round == MAX_BET:
            return ['FOLD','CALL:'+str(call_amount)]
        elif stacks[index] - call_amount < pot/2:
            return ['FOLD','CALL:'+str(call_amount),'RAISE:'+str(call_amount+2)] 
        elif stacks[index] - call_amount < pot:
            return ['FOLD','CALL:'+str(call_amount),'RAISE:'+str(call_amount+2),'RAISE:'+str(call_amount+pot/2)]
        else:
            return ['FOLD','CALL:'+str(call_amount),'RAISE:'+str(call_amount+2),'RAISE:'+str(call_amount+pot/2),'RAISE:'+str(call_amount+pot)]

            


def get_next_state(in_game_players, need_act_players, game_state, round):
    if in_game_players.count(True) == 1:
        return 'ENDGAME'
        
    if round == 'PREFLOP':
        tmp_state = 'DEALFLOP'
    elif round == 'FLOP':
        tmp_state = 'DEALTURN'
    elif round == 'TURN':
        tmp_state = 'DEALRIVER'
    elif round == 'RIVER':
        tmp_state = 'SHOWDOWN'
    else:
        print 'round is wrong'
        return
        
    if game_state == 'POSTBLINDS':
        if in_game_players[0]:
            return 'D'
        else:
            return 'SB'
    elif game_state == 'DEALFLOP' or game_state == 'DEALTURN' or game_state == 'DEALRIVER':
        if in_game_players[1]:
            return 'SB'
        else:
            return 'BB'
    elif game_state == 'D':
        if in_game_players[1]:
            if need_act_players[1]:
                return 'SB'
            else:
                return tmp_state
        else:
            if need_act_players[2]:
                return 'BB' 
            else:
                return tmp_state
    elif game_state == 'SB':
        if in_game_players[2]:
            if need_act_players[2]:
                return 'BB'
            else:
                return tmp_state
        else:
            if need_act_players[0]:
                return 'D'
            else:
                return tmp_state
    elif game_state == 'BB':
        if in_game_players[0]:
            if need_act_players[0]:
                return 'D'
            else:
                return tmp_state
        else:
            if need_act_players[1]:
                return 'SB'
            else:
                return tmp_state
    else:
        print 'Ilegal call get_next_state'
                

    
        
            
def start_new_game(stacks,gamestat):
    traverse_game_tree(stacks,[],[],[],0,'NEWGAME',' ',' ',' ',gamestat)


            
def traverse_game_tree(stacks, pot_sizes, in_game_players, need_act_players, bet_in_round, game_state, round, legal_actions, previous_actions, gamestat): 
   # print gamestat.num_flop_state
    ind = {'D':0,'SB':1,'BB':2}
    if  game_state == 'NEWGAME':
        if stacks[1] < 1 or stacks[2] < 2:
            actions = 'Error: sb or bb does not have enough stack'
            print actions
            return actions
        gamestat.set_zero()
        if stacks[0] == 0:
            print 'Dealer has no money, Enter Heads-up Game'
            traverse_game_tree(list(stacks), [0,0,0], [False, True, True], [True, True, True], 0,'DEALHAND','PREFLOP', [], ['2PGame'], gamestat)
        else:
            print 'Three Player Game'
            traverse_game_tree(list(stacks), [0,0,0], [True, True, True], [True, True, True], 0,'DEALHAND','PREFLOP', [], ['3PGame'], gamestat)
    elif game_state == 'DEALHAND':
      #  print previous_actions+[game_state]
        traverse_game_tree(list(stacks), list(pot_sizes), list(in_game_players), list(need_act_players), 0, 'POSTBLINDS','PREFLOP', [], previous_actions+[game_state], gamestat)
    elif game_state == 'POSTBLINDS':
    #    print previous_actions
        previous_actions.append('SB:POST:1')
        previous_actions.append('BB:POST:2')
       # print previous_actions
        stacks[1] -= 1
        stacks[2] -= 2        
        pot_sizes[1] += 1
        pot_sizes[2] += 2
        next_state = get_next_state(in_game_players, need_act_players, game_state, round)
        legal_actions = get_legal_actions(stacks,pot_sizes, bet_in_round,next_state)
        traverse_game_tree(stacks, [0, 1, 2], in_game_players, [True,True,True],0, next_state, 'PREFLOP', legal_actions, previous_actions,gamestat)
    elif game_state == 'DEALFLOP' or game_state == 'DEALTURN' or game_state == 'DEALRIVER':
        next_state = get_next_state(in_game_players, [True, True, True], game_state, round)
        legal_actions = get_legal_actions(stacks,pot_sizes, bet_in_round,next_state)
                
        if game_state =='DEALHAND':
            round1 = 'PREFLOP'
        elif game_state == 'DEALFLOP':
            round1 = 'FLOP'
        elif game_state == 'DEALTURN':
            round1 = 'TURN'
        else:
            round1 = 'RIVER'
        traverse_game_tree(list(stacks), list(pot_sizes), list(in_game_players), [True,True,True], 0, next_state, round1, legal_actions, previous_actions+[game_state], gamestat)
    elif game_state == 'SHOWDOWN':
        traverse_game_tree(stacks, pot_sizes, get_winners(), need_act_players, 0,'ENDGAME', 'ENDGAME', [], previous_actions+[game_state],gamestat)
    elif game_state == 'ENDGAME':
        return previous_actions + ['Player '+ str([i for i in range(0,3) if in_game_players[i]==1][0])+' wins the pot: '+ str(np.sum(pot_sizes))]
    elif game_state == 'D' or game_state =='SB' or game_state =='BB':
        count_game_state(game_state,round,gamestat)
        print ' '.join(previous_actions)
        for action in legal_actions:
            stacks_copy = list(stacks)
            pot_sizes_copy = list(pot_sizes)
            in_game_players_copy = list(in_game_players)
            need_act_players_copy = list(need_act_players)
            bet_in_round_copy = bet_in_round
            if 'FOLD' in action:
                in_game_players_copy[ind[game_state]]  = False
            elif 'CHECK' in action:
                pass
            elif 'BET' in action or 'RAISE' in action or 'CALL' in action:
                amount = int(action.split(':')[1])
                stacks_copy[ind[game_state]] -= amount
                pot_sizes_copy[ind[game_state]] += amount
                bet_in_round_copy += 1
                if 'BET' in action or 'RAISE' in action:
                    need_act_players_copy = [True, True, True]
            else:
                return 'Ilegal action' + action
            need_act_players_copy[ind[game_state]] = False
            next_state = get_next_state(in_game_players_copy, need_act_players_copy,game_state, round)
            legal_actions = get_legal_actions(stacks_copy,pot_sizes_copy, bet_in_round_copy, next_state)
            traverse_game_tree(stacks_copy,pot_sizes_copy,in_game_players_copy, need_act_players_copy, bet_in_round_copy, next_state, round, legal_actions,previous_actions + [game_state+':'+action],gamestat)
    else:
        print game_state
        print 'wrong game state'
        return
        
        
        
        
        
