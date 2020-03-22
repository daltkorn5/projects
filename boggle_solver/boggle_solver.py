#!/Users/daltkorn5/compsci/anaconda3/bin/python
import json
import sys

"""
This is a script that will find all the words on a Boggle board. It treats the game board as a graph, then uses a
modified Breadth-First-Search to find all the words on the board. It requires that you have a "dictionary.json"
file in the same directory as the script, and that the contents of that file are the game dictionary structured as a
trie. The "dictionary.json" file can be created using the "created_dictionary_file.py" and "dictionary.txt" files.

Usage:
    python boggle_solver.py [size]
"""


def load_dictionary():
    """Function that loads the dictionary file.

    :return: The game dictionary structured as a trie
    """
    with open('dictionary.json') as f:
        dictionary = json.load(f)

    return dictionary


def get_board(size):
    """Function for the user to input their game board.

    :param size: The size of the game board. In other words, the game board will be `size` x `size`
    :return: The game board represented as a 2D array. For example:
        [['a', 'b', 'c'],
         ['d', 'e', 'f'],
         ['g', 'h', 'qu']]
    """
    print("Enter your board. Put a space after each tile. After entering one row, hit enter")
    board = []

    for i in range(size):
        board.append(input().split())

    return board


def make_node(coord, letter, word, path):
    """Function to make a node for the graph that we'll use to traverse the game board.

    We have to keep path of both the `word`, because words are what we're actually searching for,
    and the `path`, so that we can make sure we don't revisit any nodes. If we were to only keep track of letters
    the search could get confused if the same letter showed up on the game board in multiple places. However, since the
    `path` is just a list of coordinates, and each coordinate is unique, we avoid this issue.

    :param coord: The (x, y) coordinate on the board
    :param letter: The letter at `coord`
    :param word: The letters seen so far on our way to `coord`
    :param path: The coordinates visited on our way to `coord`
    :return: A dict representing a node in the graph
    """
    return dict(coord=coord, letter=letter, word=word, path=path)


def get_letter(coord, board):
    """Function to get a letter on the board given the coordinate.

    :param coord: The (x, y) coordinate whose letter we want
    :param board: The game board
    :return: The letter at the given coordinate
    """
    x, y = coord
    return board[y][x]


def get_possible_moves():
    """Function that returns the list of possible moves.

    In Boggle you can form words by going up, down, right, left, or in any diagonal, so we need to check
    all of those directions in our search for successor nodes.

    :return: The list of all possible moves we could make in our search
    """
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
    """Function to check if a move is valid on our game board.

    Invalid moves are defined as moves that would go off the game board,
    or a move that would go back to coordinate we've already explored on `path`.
    This check makes it so the search doesn't go into an infinite loop (and also adheres to the Boggle rules
    where you can't reuse a letter to create a word).

    :param x_to_check: The x coordinate we're checking
    :param y_to_check: The y coordinate we're checking
    :param path: The coordinates we've visited already
    :param board: The game board
    :return: False if the move is invalid, True otherwise
    """
    if x_to_check < 0 or x_to_check >= len(board[0]):
        return False

    if y_to_check < 0 or y_to_check >= len(board):
        return False

    #  This check makes sure we don't revisit a coordinate while traversing a given path
    if (x_to_check, y_to_check) in path:
        return False

    return True


def get_successors(current_node, board):
    """Function to get the successor nodes of `current_node`.

    Checks every possible move and if that move is valid, creates a new successor node to be added
    to the search frontier.

    :param current_node: The node for which we're finding successors
    :param board: The game board
    :return: A list of all the successor nodes
    """
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
    """Function to check if our current path is worth continuing on.

    Checks if the letters in `potential_word` lead us down a branch of the dictionary. If they don't, that means
    there are no real words that start with `potential_word`, so we can throw out that search path. For example:
    If `potential_word` = 'drt' and there are no words in our dictionary that start with 'drt', we'll stop adding more
    letters to 'drt' in our search for new words.

    Additionally, if a complete word is found, that word gets added to our `words` list.

    :param potential_word: The letters we're checking to see if we've found a word, or letters that might
        lead to a word further on down in the search
    :param words: The list of we've found
    :param dictionary: The game dictionary
    :return: False if `potential_word` has no chance of leading to a real word further on down in the search,
        True otherwise
    """
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
    """Function to group the words we've found by their length.

    Used for printing out all the words of the same length on the same line.

    :param words: The list of words we found in our search.
    :return: A dict with keys as word lengths and values as the lists of words that are that long
    """
    grouped = {}
    for word in words:
        grouped.setdefault(len(word), []).append(word)

    return grouped


def pretty_print(words):
    """Function to print out the words we found in a more readable format.
    """
    grouped_words = group_words_by_length(words)
    for length, word_list in sorted(grouped_words.items()):
        print(", ".join(sorted(word_list)))


def main():
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    else:
        size = 4

    dictionary = load_dictionary()

    board = get_board(size)

    words = []

    coords = [(x, y) for y in range(len(board)) for x in range(len(board[0]))]
    for start in coords:
        for goal in coords:
            find_all_words(start, goal, words, board, dictionary)

    pretty_print(set(words))


if __name__ == '__main__':
    main()
