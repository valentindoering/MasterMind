def print_list(li, print_func=print):
    print_func('[\n\t' + ',\n\t'.join(list(map(str, li))) + '\n]')