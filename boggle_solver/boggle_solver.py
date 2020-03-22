#!/Users/daltkorn5/compsci/anaconda3/bin/python
import json
from time import time


def load_dictionary():
    with open('dictionary.json') as f:
        words = json.load(f)

    return words


def get_board(size=4):
    print("Enter your board. Put a space after each tile. After entering one row, hit enter")
    board = []
    i = 0

    while i < size:
        board.append(input().split())
        i += 1

    return board


def make_node(coord, letter, word, path):
    """Function to make a node for the graph that we'll use to traverse the game board.

    :param coord: The (x, y) coordinate on the board
    :param letter: The letter at coord
    :param word: The letters seen so far on our way to coord
    :param path: The coordinates visited on our way to coord
    :return: A dict representing a node in the graph
    """
    return dict(coord=coord, letter=letter, word=word, path=path)


def get_letter(coord, board):
    """Function to get a letter on the board given the coordinate

    :param coord: The (x, y) coordinate whose letter we want
    :param board: The game board
    :return: The letter at the given coordinate
    """
    x, y = coord
    return board[y][x]


def is_goal(current_node, goal):
    return current_node['coord'] == goal


def get_possible_moves():
    return [
        (-1, -1),  # up and to the left
        (-1, 0),  # directly to the left
        (-1, 1),  # down and to the left
        (0, 1),  # directly down
        (1, 1),  # down and to the right
        (1, 0),  # directly to the right
        (1, -1),  # down and to the right
        (0, -1)  # directly up
    ]


def is_valid_move(x_to_check, y_to_check, path, board):
    if x_to_check < 0 or x_to_check >= len(board[0]):
        return False

    if y_to_check < 0 or y_to_check >= len(board):
        return False

    #  This check makes sure we don't revisit a coordinate while traversing a given path
    if (x_to_check, y_to_check) in path:
        return False

    return True


def get_successors(current_node, board):
    possible_moves = get_possible_moves()
    successors = []
    
    for move in possible_moves:
        current_coord = current_node['coord']
        x_to_check = current_coord[0] + move[0]
        y_to_check = current_coord[1] + move[1]

        if is_valid_move(x_to_check, y_to_check, current_node['path'], board):
            new_coord = (x_to_check, y_to_check)
            new_letter = get_letter(new_coord, board)
            new_node = make_node(new_coord, new_letter,
                                 current_node['word'] + new_letter, current_node['path'] + [new_coord])

            successors.append(new_node)

    return successors


def check_is_search_fruitful(potential_word, words, dictionary):
    current_dict = dictionary
    for letter in potential_word.upper():
        if letter not in current_dict:
            return False

        current_dict = current_dict[letter]

    if "end" in current_dict:
        words.append(potential_word)

    return True


def find_all_words(start, goal, words, board, dictionary):
    """Function to find all the words between the starting letter and the goal letter.

    We'll use a Breadth-First-Search approach for traversing our graph. As we're not trying to find the
    most efficient path between the start and the goal, we don't need to use an informed search like A*.

    :param start: The starting coordinate
    :param goal: The goal coordinate
    :param words: List of valid words we've found in our search
    :param board: The game board
    :param dictionary: The game dictionary (like a real dictionary, not a python object)
    """
    if start == goal:
        return
    starting_letter = get_letter(start, board)
    initial_node = make_node(start, starting_letter, starting_letter, [start])
    frontier = [initial_node]  # The frontier of our BFS, a list of which coordinates will be checked next

    while len(frontier) > 0:
        # Since BFS uses a FIFO queue for choosing its next node to explore
        # we pop off the last node in the frontier list
        current_node = frontier.pop()

        successors = get_successors(current_node, board)
        for successor in successors:
            if check_is_search_fruitful(successor['word'], words, dictionary):
                frontier.insert(0, successor)


def group_words_by_length(words):
    grouped = {}
    for word in words:
        grouped.setdefault(len(word), []).append(word)

    return grouped


def pretty_print(words):
    grouped_words = group_words_by_length(words)
    for length, word_list in sorted(grouped_words.items()):
        print(", ".join(sorted(word_list)))


def main():
    dictionary = load_dictionary()

    board = get_board()
    # board = [['d', 'e', 'l', 'b'],
    #          ['a', 'n', 't', 'o'],
    #          ['z', 'qu', 'i', 'k'],
    #          ['e', 'p', 'c', 'x']]
    # board = [['d', 'e', 'l'],
    #          ['a', 'n', 't'],
    #          ['z', 'qu', 'i']]

    words = []

    st = time()
    coords = [(x, y) for y in range(len(board)) for x in range(len(board[0]))]
    for start in coords:
        for goal in coords:
            find_all_words(start, goal, words, board, dictionary)

    pretty_print(set(words))
    end = time()
    print(end - st)


if __name__ == '__main__':
    main()
