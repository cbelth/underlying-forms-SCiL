from alphabet import Alphabet
from sequence import Sequence

class Form:
    '''
    A class representing a WordForm.
    '''
    def __init__(self, form, segmentation, analysis, alphabet=None):        
        self.alphabet = alphabet if alphabet is not None else Alphabet()
        self.alphabet.add_segments_from_str(form)
        self.form = Sequence(form, alphabet=self.alphabet)
        self.is_stem = analysis == 'Stem'
        self.is_affix = not self.is_stem
        self.segmentation, self.analysis = list(), list()
        for s, a in zip(segmentation.split('-'), analysis.split('-')):
            self.alphabet.add_segments_from_str(s) 
            self.segmentation.append(Sequence(s, alphabet=self.alphabet))
            self.analysis.append(a)

    def __str__(self):
        return f'{self.form}'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.form)

    def __eq__(self, other):
        if type(other) is not Form:
            return False
        return self.form == other.form and self.analysis == other.analysis

    def __neq__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(f'form_{self.form}_{self.analysis}')

    def __lt__(self, other):
        return f'{self} / {self.analysis}' < f'{other} / {self.analysis}'

    def parts(self):
        return list(zip(self.segmentation, self.analysis))
