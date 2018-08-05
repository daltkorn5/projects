#!/usr/bin/python

import json

BOARD_SIZE = 4

def main():

    dictionary = load_dictionary()

    #board = get_board()
    board = [['d', 'e', 'l', 'b'],
             ['a', 'n', 't', 'o'],
             ['z', 'qu', 'i', 'k'],
             ['e', 'p', 'c', 'x']]
    board_graph = board_to_graph(board)
    board_lookup = get_board_coord_to_letter_lookup_hash(board)

    words = []
    for key1 in board_graph:
        for key2 in board_graph:
            if key1 == key2: continue
            paths, new_words = find_all_words(board_graph, key1, key2, dictionary, board_lookup)
            words.extend(new_words)

    words.sort(key = lambda s: (len(s), s[0]))

    pretty_print(set(words))

def load_dictionary():

    with open('dictionary.json') as f:
        words = json.load(f)

    return words

def get_board():

    print "Enter your board. After entering one row, hit enter"
    board = []
    i = 0

    while i < BOARD_SIZE:
        board.append(raw_input().split())
        i += 1

    return board

def board_to_graph(board):
    graph = {}

    coords_to_check = [(-1, -1), # up and to the left
                       (-1,  0), # directly to the left
                       (-1,  1), # down and to the left
                       (0,   1), # directly down
                       (1,   1), # down and to the right
                       (1,   0), # directly to the right
                       (1,  -1), # down and to the right
                       (0,  -1)] # directly up

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # need a unique identifier for each tile in case there are duplicate letters
            tile_coord = get_unique_board_coord(row, col)

            graph[tile_coord] = []

            for coord in coords_to_check:
                row_to_check = row + coord[0]
                col_to_check = col + coord[1]
                if is_valid_coord(row_to_check, col_to_check):
                    graph[tile_coord].append(get_unique_board_coord(row_to_check, col_to_check))

    return graph

def get_unique_board_coord(row, col):

    return BOARD_SIZE * row + col

def is_valid_coord(row, col):

    if row < 0 or row >= BOARD_SIZE:
        return False

    if col < 0 or col >= BOARD_SIZE:
        return False

    return True

def get_board_coord_to_letter_lookup_hash(board):

    lookup = {}

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            tile_coord = get_unique_board_coord(row, col)
            lookup[tile_coord] = board[row][col]

    return lookup

def find_all_words(graph, start, end, dictionary, lookup, path = []):
    # adapted from https://www.python.org/doc/essays/graphs/
    path = path + [start]
    if start == end:
        return [path], [lookup[x] for x in path]
    if not graph.has_key(start):
        return [], []
    paths = []
    words = []
    for node in graph[start]:
        if node not in path:
            newpaths, new_words = find_all_words(graph, node, end, dictionary, lookup, path)
            for newpath in newpaths:
                potential_word = "".join(lookup[x] for x in newpath)
                paths.append(newpath)
                if is_word(potential_word, dictionary):
                    words.append(potential_word)
    return paths, words

def is_word(word, dictionary):

    try:
        first_letter = word[:1]
        first_two_letters = word[:2]
        dictionary[first_letter][first_two_letters][word]
    except KeyError:
        return False

    return True

def pretty_print(words):

    print # newline to separate from board input

    words_by_length = group_words_by_length(words)

    longest_word_length = max(key for key in words_by_length)
    group_with_most_words = max(words_by_length, key = lambda x: len(words_by_length[x]))

    for row in range(len(words_by_length[group_with_most_words])):
        for col in range(3, longest_word_length + 1):

            if row >= len(words_by_length[col]): continue
            print words_by_length[col][row] + "  ",
        print

def group_words_by_length(words):

    words_group = {}
    for w in words:
        if len(w) not in words_group: words_group[len(w)] = []
        words_group[len(w)].append(w)

    return words_group


if __name__ == '__main__':
    main()
