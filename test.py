import itertools
import random
from utils import print_list
from main import get_all_combinations, is_valid_combi, get_filter, get_most_different_combi, feedback, del_idxs_from_list
from functools import reduce


def get_all_feedback_permus(n_red, n_white, total):
    '''
    This function returns all possible feedback permutations.
    '''
    feedback = ['empty'] * (total - n_red - n_white)
    feedback.extend(['red'] * n_red)
    feedback.extend(['white'] * n_white)
    return list(set(itertools.permutations(feedback)))

def test_is_valid_combi():
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'white']
    n_digits_code = 5

    # guessed_combi = ['yellow', 'orange', 'yellow', 'pink', 'green']
    # feedback_sticks = ['empty', 'red', 'empty', 'white', 'red']

    # print('True', is_valid_combi(guessed_combi, feedback_sticks, ['orange', 'white', 'green', 'pink', 'blue']))
    # print('False', is_valid_combi(guessed_combi, feedback_sticks, ['orange', 'white', 'pink', 'yellow', 'pink']))

    # print('True', is_valid_combi(guessed_combi, feedback_sticks, ['orange', 'orange', 'pink', 'blue', 'green']))
    # print('False', is_valid_combi(guessed_combi, feedback_sticks, ['orange', 'orange', 'pink', 'pink', 'green']))

    guessed_combi = ['white', 'green', 'orange', 'purpel', 'white']
    feedback_permus = get_all_feedback_permus(n_red=1, n_white=2, total=len(guessed_combi))
    combi_to_check = ['purple', 'orange', 'pink', 'purple', 'white']
    for feedback_sticks in feedback_permus:
        print(list(zip(guessed_combi, feedback_sticks)))
        print(is_valid_combi(guessed_combi, feedback_sticks, ['white', 'green', 'orange', 'purpel', 'white']))

def test_get_all_combination():
    # colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'white', 'black', 'brown', 'gray']
    colors = ['black', 'yellow', 'orange', 'dark_red', 'red', 'green', 'white', 'grey', 'brown', 'dark_green', 'blue']
    n_digits_code = 4
    all_combinations = get_all_combinations(colors, n_digits_code)
    print('len', len(all_combinations))
    print('len(colors)', len(colors))
    print('n_digits_code', n_digits_code)
    print('should be (n_digits_code ** len(colors))', len(colors) ** n_digits_code)



def test_get_most_different_combi():
    guesses = [
        ('red', 'green', 'blue', 'white', 'yellow'),
        ('red', 'blue', 'white', 'red', 'red')
    ]

    all_combis = get_all_combinations(colors = ['black', 'yellow', 'orange', 'dark_red', 'red', 'green', 'white', 'grey', 'brown', 'dark_green', 'blue'], n_digits_code = 4)
    
    print(get_most_different_combi(guesses, all_combis))

    # print(get_next_guess(guesses, remaining_combis))
    # print(reduce(lambda x, y: x + y, [1, 2, 3], 1))


def test_feedback():
    # feedback(combi, guess)
    print('red: 2, white: 1', feedback(['red', 'green', 'blue', 'white'], ['red', 'white', 'blue', 'red']))
    print('red: 0, white: 0', feedback(['red', 'green', 'blue', 'white'], ['yellow', 'purple', 'brown', 'pink']))
    print('red: 4, white: 0', feedback(['red', 'green', 'blue', 'white'], ['red', 'green', 'blue', 'white']))
    print('red: 1, white: 3', feedback(['red', 'green', 'blue', 'white'], ['green', 'blue', 'red', 'white']))

def test_del_idxs_from_list():
    li = ['a', 'b', 'c', 'd', 'e']
    print(li)
    del_idxs_from_list(li, [0, 2, 4])
    print(li)

test_del_idxs_from_list()



