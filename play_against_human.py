from main import mastermind

def play_against_human():
    colors = ['black', 'yellow', 'orange', 'dark_red', 'red', 'green', 'white', 'grey', 'brown', 'dark_green', 'blue']
    n_digits_code = 4
    mastermind(colors, n_digits_code, print_func=print)

play_against_human()