'''
    This programm should be able to guess a n_digits_code digit Mastermind color code.
    In each iteration the programm should give a guess and the user should enter the feedback as 
        - n_red (number of pearls with correct color and correct position), 
        - n_white (number of pearls with correct color but wrong position).
    The programm should stop, when the feedback is n_red = n_digits_code (code correct guessed).
'''

import itertools
import random
from utils import print_list
from functools import reduce


def get_all_combinations(colors, n_digits_code):
    '''
    This function returns all possible combinations of colors and numbers.
    '''
    all_combinations = []
    for i in range(n_digits_code):
        all_combinations.append(colors)
    return list(itertools.product(*all_combinations))

def is_valid_combi(guessed_combi, feedback_sticks, combi_to_check):
    # correct elements ------------------------------------------------
    must_be_in_combi = []
    must_not_be_in_combi = []
    for color, stick in zip(guessed_combi, feedback_sticks):
        must_not_be_in_combi.append(color) if stick == 'empty' else must_be_in_combi.append(color)

    combi_copy = list(combi_to_check)
    for color in must_be_in_combi:
        if color not in combi_copy: 
            return False
        else: 
            combi_copy.remove(color)
    
    for color in must_not_be_in_combi:
        if color in combi_copy:
            return False

    # correct positioning ------------------------------------------------
    for i, color, stick in zip(range(len(guessed_combi)), guessed_combi, feedback_sticks):
        if (stick == 'red' and combi_to_check[i] != color) or \
                (stick == 'white' and combi_to_check[i] == color):
            return False

    # all tests passed
    return True

def get_filter(guessed_combi, n_red, n_white):
    n_empty = len(guessed_combi) - n_red - n_white
    if n_empty < 0:
        raise ValueError('n_empty < 0')
    
    feedback = ['empty'] * n_empty
    feedback.extend(['red'] * n_red)
    feedback.extend(['white'] * n_white)
    feedback_permutations = list(set(itertools.permutations(feedback))) # this is unefficient!

    def filter_fun(combi_to_check):
        for feedback_sticks in feedback_permutations:
            if is_valid_combi(guessed_combi, feedback_sticks, combi_to_check):
                return True
        return False
    return filter_fun

def get_most_different_combi(guesses, combinations):
    '''
    score = color_diversity + color_positioning
    '''
    color_diversity = lambda combi: len(set(combi)) # from 1 to n_digits_code
    guesses_dict = {} # {'red': [0, 2], 'white': [3, 4]}
    for guess in guesses:
        for i, color in enumerate(guess):
            if color not in guesses_dict:
                guesses_dict[color] = [i]
            else:
                if i not in guesses_dict[color]:
                    guesses_dict[color].append(i)
    
    def score(combi):
        score = color_diversity(combi)
        for idx, color in enumerate(combi):
            if color not in guesses_dict:
                score += 1
            else:
                if idx in guesses_dict[color]:
                    score -= 1
        return score

    combinations = list(map(lambda combi: (combi, score(combi)), combinations))
    # sorted_combinations = sorted(combinations, key=lambda combi: combi[1])
    # print('best scores')
    # print_list(sorted_combinations[:100])
    # print('worst scores')
    # print_list(sorted_combinations[-100:])
    # print(guesses_dict)
    return max(combinations, key=lambda combi_score: combi_score[1])[0]
    


def print_history(history, last_guess):
    n_rounds_outer = None
    for n_rounds, guess, n_red, n_white, n_remaining_before, n_remaining_after in history:
        print('Round {}, Guess: {}, N_red: {}, N_white: {}, N_remaining_before {}, N_remaining_after {}'.format(n_rounds, guess, n_red, n_white, n_remaining_before, n_remaining_after), end='\n\n')
        n_rounds_outer = n_rounds + 1
    print('Round {}, Guess (that was right) {}'.format(n_rounds_outer, last_guess))

def mastermind(colors, n_digits_code, feedback_func=None, print_func=print):
    print_func('\nSTART MASTERMIND ===========================================================\n')
    sample_print_size = 10

    all_combinations = get_all_combinations(colors, n_digits_code)
    remaining_combinations = all_combinations
    history = []
    n_rounds = 0
    guesses = []

    while True:
        n_rounds += 1
        print_func('\nRound:', n_rounds, '===========================================\n')

        if len(remaining_combinations) == 0:
            print_func('No more combinations left!', '\n')
            print_history(history, guess)
            break

        print_func('Remaining combinations this round (', len(remaining_combinations), '):')
        if len(remaining_combinations) < sample_print_size:
            print_list(remaining_combinations, print_func=print_func)
            print_func('(', len(remaining_combinations), ')\n')
        else:
            print_list(random.sample(remaining_combinations, sample_print_size), print_func=print_func)
            print_func('Ouput too long, printing sample')
            print_func('(', len(remaining_combinations), ')\n')

        # next guess ------------------------------------------------

        guess = None
        if n_rounds == 1 or (n_rounds <= 2 and history[-1][2] + history[-1][3] < n_digits_code):
            guess = get_most_different_combi(guesses, all_combinations)
        else:
            guess = get_most_different_combi(guesses, remaining_combinations)

        # guess = get_most_different_combi(guesses, remaining_combinations)

        # guess = random.choice(remaining_combinations)
        guesses.append(guess)
        print_func('I decide on the guess: ', guess, '\n')
        # ------------------------------------------------------------

        n_red = int(input('How many reds? ')) if feedback_func == None else feedback_func(guess)[0]
        if n_red == n_digits_code:
            print_func('I guessed it!')
            print_history(history, guess)
            return n_rounds
        n_white = int(input('How many whites? ')) if feedback_func == None else feedback_func(guess)[1]

        n_remaining_before = len(remaining_combinations)
        filter_fun = get_filter(guess, n_red, n_white) # returns true, if combination still valid (stays in list)
        remaining_combinations = list(filter(filter_fun, remaining_combinations))
        n_remaining_after = len(remaining_combinations)
        history.append((n_rounds, guess, n_red, n_white, n_remaining_before, n_remaining_after))

def del_idxs_from_list(my_list, indexes):
    for index in sorted(indexes, reverse=True):
        del my_list[index]

def feedback(combi, guess):
    combi = list(combi)
    guess = list(guess)

    n_red = 0
    n_white = 0
    del_indexes = []
    for i in range(len(combi)):
        if combi[i] == guess[i]:
            del_indexes.append(i)
            n_red += 1
    del_idxs_from_list(combi, del_indexes)
    del_idxs_from_list(guess, del_indexes)

    while len(guess) > 0:
        if guess[0] in combi:
            n_white += 1
            combi.remove(guess[0])
        del guess[0]
    return n_red, n_white
