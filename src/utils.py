from itertools import chain, combinations
import numpy as np

LEFT_WORD_BOUNDARY = '⋊'
RIGHT_WORD_BOUNDARY = '⋉'
SYLLABLE_BOUNDARY = '.'
PRIMARY_STRESS = 'ˈ'
SECONDARY_STRESS = 'ˌ'
LONG = 'ː'
NASALIZED = '\u0303'
EMPTY_STRING = '∅'
UNKNOWN_CHAR = '?'
NEG_SYMBOL = '¬'

def load(fname, sep='\t', skip_header=False):
    words = list()
    freqs = list()
    with open(fname, 'r') as f:
        if skip_header:
            next(f)
        for line in f:
            word, num, sg, pl, freq = line.strip().split(sep)
            freq = float(freq)
            words.append((word, num, sg, pl))
            freqs.append(freq)
    return words, freqs

def tolerance_principle(n, c=None, e=None):
    if c is None and e is None:
        raise ValueError(f'c and e cannot both be None.')
    if e is None:
        e = n - c
    if c is None:
        c = n - e
    return c > 1 and e <= n / np.log(n) and c > n / 2

def epsilon(n, c, eps=0.99):
    if n == c:
        return True
    return c > 2 and c / n >= eps

def sufficiency_principle(n, m):
    return m > 2 and m > n / 2 and n - m < n / np.log(n)

def powerset(iterable, smallest=0, largest=None, proper_subset_only=False):
    '''
    Adapted From: https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    '''
    s = list(iterable)
    if largest == None:
        largest = len(s) + 1 if not proper_subset_only else len(s)
    return set(chain.from_iterable(combinations(s, r) for r in range(smallest, largest)))

def align_blanks(s1, s2, return_ties=False):
    '''
    Add blanks (EMPTY_STRING), so that s1 and s2 are optimaly aligned and of the same length.
    Assumes that len(s1) < len(s2).
    '''
    delta = len(s2) - len(s1)
    options = sorted(insert_empty(s1, k=delta), key=lambda op: (hd(op, s2), op.index(EMPTY_STRING)))
    if return_ties and len(options) > 1:
        res = [options[0]]
        i = 1
        while i < len(options) and hd(options[i], s2) == hd(options[0], s2):
            res.append(options[i])
            i += 1
        return res
    return options[0]

def longest_common_prefix(strings):
    lcp = ''
    i = 0

    min_len = min(len(s) for s in strings)
    while i < min_len:
        target_char = strings[0][i]
        if all(s[i] == target_char for s in strings):
            lcp += target_char
            i += 1
        else:
            break
    return lcp