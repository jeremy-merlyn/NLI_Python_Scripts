import itertools
import sys
import csv

from nltk.grammar import Nonterminal, CFG

def generate(grammar, start=None, depth=None, n=None):
    """
    Generates an iterator of all sentences from a CFG.
    :param grammar: The Grammar used to generate sentences.
    :param start: The Nonterminal from which to start generate sentences.
    :param depth: The maximal depth of the generated tree.
    :param n: The maximum number of sentences to return.
    :return: An iterator of lists of terminal tokens.
    """
    if not start:
        start = grammar.start()
    if depth is None:
        depth = sys.maxsize

    iter = _generate_all(grammar, [start], depth)

    if n:
        iter = itertools.islice(iter, n)

    return iter


def _generate_all(grammar, items, depth):
    if items:
        try:
            for frag1 in _generate_one(grammar, items[0], depth):
                for frag2 in _generate_all(grammar, items[1:], depth):
                    yield frag1 + frag2
        except RecursionError as error:
            # Helpful error message while still showing the recursion stack.
            raise RuntimeError(
                "The grammar has rule(s) that yield infinite recursion!"
            ) from error
    else:
        yield []


def _generate_one(grammar, item, depth):
    if depth > 0:
        if isinstance(item, Nonterminal):
            for prod in grammar.productions(lhs=item):
                yield from _generate_all(grammar, prod.rhs(), depth - 1)
        else:
            yield [item]


def generate_list(filename, N=1000):

    with open(filename, 'r') as file:
        lines = ''
        for line in file:
            if not line.startswith("#"):
                lines += line
        grammar = CFG.fromstring(lines)

    sents = [" ".join(sent) for sent in generate(grammar, n=N)]
    return sents


def make_csv(cases, csv_name):
    with open(csv_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['UTTERANCE'])
        for text in cases:
            csvwriter.writerow([text])

def make_csv_from_grammar(filename):
    examples = generate_list(filename, N=1500)
    make_csv(examples, filename.split('_psg.txt')[0]+'.csv')

if __name__ == "__main__":
    # print(generate_list('PSG/svolume_psg.txt'))
    pass