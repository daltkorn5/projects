#!/usr/bin/python

import json

def main():

    words = get_words()
    words_dict = arrange_words_into_dict(words)
    write_file(words_dict)

def get_words():

    with open('dictionary.txt') as f:
        words = f.read().split('\n')

    return words

def arrange_words_into_dict(words):

    words_dict = {}

    for word in words:
        if len(word) < 3: continue # don't care about words less than 3 letters long in boggle!

        first_letter = word[:1]
        if first_letter not in words_dict:
            words_dict[first_letter] = {}

        first_two_letters = word[:2]
        if first_two_letters not in words_dict[first_letter]:
            words_dict[first_letter][first_two_letters] = {}

        words_dict[first_letter][first_two_letters][word.lower()] = 1

    return words_dict

def write_file(words_dict):

    with open('dictionary.json', 'w') as f:
        f.write(json.dumps(words_dict))

if __name__ == '__main__':
    main()
