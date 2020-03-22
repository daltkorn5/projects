#!/Users/daltkorn5/compsci/anaconda3/bin/python
import json


def get_words():
    with open('dictionary.txt') as f:
        words = f.read().split('\n')

    return words


def arrange_words_into_trie(words):
    root = {}
    for word in words:
        # we don't care about words with fewer than 3 letters in Boggle
        if len(word) < 3:
            continue
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict['end'] = True
    return root


def write_file(words_dict):
    with open('dictionary.json', 'w') as f:
        f.write(json.dumps(words_dict))


def main():
    words = get_words()
    trie = arrange_words_into_trie(words)
    write_file(trie)


if __name__ == '__main__':
    main()
