from audioop import add
import unittest
import sys
sys.path.append('../src/')
from alphabet import Alphabet

class TestAlphabet(unittest.TestCase):
    def test_getitem_1(self):
        alphabet = Alphabet(add_segs=True)

        b = alphabet['b']
        assert(alphabet['b'].ipa == 'b')
        assert(alphabet[','.join(b.feature_vec)].ipa == 'b')
        assert(alphabet[b.feature_vec].ipa == 'b')
        assert(alphabet[b] == b)

        p = alphabet['p']
        assert(alphabet['p'].ipa == 'p')
        assert(alphabet[','.join(p.feature_vec)].ipa == 'p')
        assert(alphabet[p.feature_vec].ipa == 'p')
        assert(alphabet[p] == p)

    def test_without_feats_1(self):
        alphabet = Alphabet(add_segs=True)

        b = alphabet['b']
        p = alphabet['p']

        assert(alphabet.without_feats('b', 'voice') == p)
        assert(alphabet.without_feats(','.join(b.feature_vec), 'voice') == p)
        assert(alphabet.without_feats(b.feature_vec, 'voice') == p)

    def test_with_feats_1(self):
        alphabet = Alphabet(add_segs=True)

        b = alphabet['b']
        p = alphabet['p']

        assert(alphabet.with_feats('p', 'voice') == b)
        assert(alphabet.with_feats(','.join(p.feature_vec), 'voice') == b)
        assert(alphabet.with_feats(p.feature_vec, 'voice') == b)

    def test_assimilate_1(self):
        alph = Alphabet('../data/ipa.txt', add_segs=True)

        assert(alph.assimilate('I', 'i', 'back') == 'i')
        assert(alph.assimilate('I', 'ɯ', 'back') == 'ɯ')
        assert(alph.assimilate('k', 'ɯ', 'back') == None)

    def test_dissimilate_1(self):
        alph = Alphabet(add_segs=True)

        assert(alph.dissimilate('d', 'd', 'voice') == 't')
        assert(alph.dissimilate('g', 'd', 'voice') == 'k')
        assert(alph.dissimilate('m', 'd', 'voice') == None)

    def test_dissimilate_3(self):
        alph = Alphabet(ipa_file='../data/ipa.txt', add_segs=True)

        assert(alph.dissimilate('r', 'r', ('ant', 'lat')) == 'l')
        assert(alph.dissimilate('l', 'l', ('ant', 'lat')) == 'r')

if __name__ == "__main__":
    unittest.main()