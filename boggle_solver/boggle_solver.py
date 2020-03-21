#!/Users/daltkorn5/compsci/anaconda3/bin/python

import json

BOARD_SIZE = 4


def main():
    dictionary = load_dictionary()

    # board = get_board()
    board = [['d', 'e', 'l', 'b'],
             ['a', 'n', 't', 'o'],
             ['z', 'qu', 'i', 'k'],
             ['e', 'p', 'c', 'x']]

    board_graph = board_to_graph(board)

    words = []

    # check for all paths between each pair of letters on the board
    for letter1 in board_graph:
        for letter2 in board_graph:
            if letter1 == letter2: continue
            new_words = find_all_words(board_graph, letter1, letter2, dictionary)
            words.extend(new_words)

    pretty_print(set(words))


def load_dictionary():
    with open('dictionary.json') as f:
        words = json.load(f)

    return words


def get_board():
    print("Enter your board. After entering one row, hit enter")
    board = []
    i = 0

    while i < BOARD_SIZE:
        board.append(input().split())
        i += 1

    return board


def board_to_graph(board):
    """convert the board into a graph represented using adjacency lists"""

    graph = {}

    coords_to_check = [(-1, -1),  # up and to the left
                       (-1, 0),  # directly to the left
                       (-1, 1),  # down and to the left
                       (0, 1),  # directly down
                       (1, 1),  # down and to the right
                       (1, 0),  # directly to the right
                       (1, -1),  # down and to the right
                       (0, -1)]  # directly up

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # need a unique identifier for each tile in case there are duplicate letters
            tile_coord = get_unique_board_coord(row, col)

            graph[tile_coord] = {
                "letter": board[row][col],
                "adjacent_letters": []
            }

            for coord in coords_to_check:
                row_to_check = row + coord[0]
                col_to_check = col + coord[1]
                if is_valid_coord(row_to_check, col_to_check):
                    graph[tile_coord]["adjacent_letters"].append(get_unique_board_coord(row_to_check, col_to_check))

    return graph


def get_unique_board_coord(row, col):
    return BOARD_SIZE * row + col


def is_valid_coord(row, col):
    if row < 0 or row >= BOARD_SIZE:
        return False

    if col < 0 or col >= BOARD_SIZE:
        return False

    return True


def find_all_words(graph, starting_node, ending_node, dictionary, path=[], word=''):
    # adapted from https://www.python.org/doc/essays/graphs/

    if starting_node == ending_node:
        return [word]

    if not graph.has_key(starting_node):
        return []

    path = path + [starting_node]
    word = word + graph[starting_node]["letter"]

    words = []

    adjacent_letters = graph[starting_node]["adjacent_letters"]
    for node in adjacent_letters:

        if node not in path:
            new_words = find_all_words(graph, node, ending_node, dictionary, path, word)

            for w in new_words:
                if is_word(w, dictionary):
                    words.append(w)

    return words


def is_word(word, dictionary):
    try:
        first_letter = word[:1].upper()
        first_two_letters = word[:2].upper()
        dictionary[first_letter][first_two_letters][word]
    except KeyError:
        return False

    return True


def pretty_print(words):
    print()  # newline to separate from board input

    words_by_length = group_words_by_length(words)

    longest_word_length = max(key for key in words_by_length)
    group_with_most_words = max(words_by_length, key=lambda x: len(words_by_length[x]))

    for row in range(len(words_by_length[group_with_most_words])):
        for col in range(3, longest_word_length + 1):

            if row >= len(words_by_length[col]): continue
            print(words_by_length[col][row] + "  ", end="")
        print()

    print()


def group_words_by_length(words):
    words_group = {}
    for w in words:
        if len(w) not in words_group: words_group[len(w)] = []
        words_group[len(w)].append(w)

    return words_group


if __name__ == '__main__':
    main()
