from main import mastermind, get_all_combinations, feedback
import random

def play_simulation(n_times=1000):

    # colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'white']
    colors = ['black', 'yellow', 'orange', 'dark_red', 'red', 'green', 'white', 'grey', 'brown', 'dark_green', 'blue']
    n_digits_code = 4

    n_rounds_needed = []
    all_combinations = get_all_combinations(colors, n_digits_code)

    for i in range(n_times):
        goal_combi = random.choice(all_combinations)
        print('\n\n', 'NEW GAME WITH ========================> Goal combi: ', goal_combi, '\n')

        feedback_func = lambda guess: feedback(goal_combi, guess)
        n_rounds_needed.append(mastermind(colors, n_digits_code, feedback_func, print_func=lambda *args: None))

    print('===========================================')
    print('Average number of rounds needed: ', sum(n_rounds_needed) / len(n_rounds_needed))
    print('rounds needed: ', n_rounds_needed)
    print('===========================================')

play_simulation()


