import unittest
import sys
sys.path.append('../src/')
from form import Form
from morpheme import Morpheme
from alphabet import Alphabet

class TestMorpheme(unittest.TestCase):
    def test_abstract_pl(self):
        alph = Alphabet(ipa_file='../data/ipa.txt', add_segs=True)
        lar = Form('lɑr', segmentation='-lɑr', analysis='-pl', alphabet=alph)
        ler = Form('ler', segmentation='-ler', analysis='-pl', alphabet=alph)
        pl = Morpheme(form=lar)
        pl.add_form(form=lar)
        pl.add_form(form=lar)
        pl.add_form(form=ler)
        pl.add_form(form=ler)
        pl.add_form(form=ler)
        pl.add_form(form=lar)
        pl.add_form(form=ler)
        assert(pl.form == 'lAr')

    def test_abstract_gen(self):
        alph = Alphabet(ipa_file='../data/ipa.txt', add_segs=True)
        f1 = Form('in', segmentation='-in', analysis='-gen', alphabet=alph)
        f1_ep = Form('nin', segmentation='-nin', analysis='-gen', alphabet=alph)
        f2 = Form('un', segmentation='-un', analysis='-gen', alphabet=alph)
        f2_ep = Form('nun', segmentation='-nun', analysis='-gen', alphabet=alph)
        gen = Morpheme(form=f1)
        for _ in range(14):
            gen.add_form(f1)
        for _ in range(9):
            gen.add_form(f1_ep)
        for _ in range(2):
            gen.add_form(f2)
        for _ in range(3):
            gen.add_form(f2_ep)
        assert(gen.form == 'Hn')

if __name__ == "__main__":
    unittest.main()