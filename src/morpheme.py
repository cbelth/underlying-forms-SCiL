from collections import defaultdict
from utils import EMPTY_STRING
import numpy as np

class Morpheme:
    '''
    A class representing a morpheme.
    '''
    def __init__(self, form, feat=None, concrete=True):
        self.alphabet = form.alphabet
        self.null = False # track whether morpheme has a null (emtpy) form
        if form == '':
            form = ''
            self.null = True
        self.feat = feat if feat is not None else 'Stem'
        self.is_stem = self.feat == 'Stem'
        self.is_affix = not self.is_stem
        self._forms = defaultdict(int)
        self.add_form(form)
        self.concrete = concrete

    def __str__(self):
        return f'{self.form}' if self.is_stem else f'-{self.form}'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.form)

    def __eq__(self, other):
        if type(other) is str:
            return self.feat == other
        if type(other) is not Morpheme:
            return False
        if self.is_stem:
            return other.is_stem and self.form == other.form
        return other.is_affix and self.feat == other.feat

    def __neq__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self.is_stem:
            return hash(f'stem_morpheme_{self.form}')
        return hash(f'{self.feat}')

    def __lt__(self, other):
        return f'{self}' < f'{other}'

    def collapse_into_abstract(self):
        def _abstractify(_segs, _seg_freqs):
            vec = ['?'] * len(self.alphabet.feature_space)
            feat_diff = set()
            for idx, feat in enumerate(self.alphabet.feature_space):
                vals = list(set(self.alphabet.get_val(seg, feat) for seg in _segs))
                val = vals[0] if len(vals) == 1 else '?'
                if len(vals) > 1:
                    feat_diff.add(feat)
                vec[idx] = val
            _argmax, _max = sorted(_seg_freqs.items(), reverse=True, key=lambda it: (it[-1], it[0]))[0]
            if len(feat_diff) > 3:
                return _argmax

            if vec in self.alphabet:
                return f'{self.alphabet[vec]}'
            else:
                if self.alphabet.add_underspec(vec):
                    return f'{self.alphabet[vec]}'
                else:
                    raise ValueError(f'Unable to form abstract UR for {self.feat} with forms {self._forms}')

        ur = ''
        len_freq = defaultdict(int)
        for form, freq in self._forms.items():
            len_freq[len(form)] += freq
        l = sorted(len_freq.items(), reverse=True, key=lambda it: it[-1])[0][0]
        aligned_forms = list()
        for form in self._forms.keys():
            aligned_form = f'{form}'
            while len(aligned_form) < l:
                aligned_form = f'{EMPTY_STRING}{aligned_form}'
            while len(aligned_form) > l:
                aligned_form = aligned_form[1:]
            aligned_forms.append(list(aligned_form))
        aligned_forms = np.asarray(aligned_forms)
                    
        for idx in range(l):
            _segs = set()
            _seg_freqs = defaultdict(int)
            for form_idx, form in enumerate(self._forms.keys()):
                seg = str(aligned_forms[form_idx,idx])
                if seg != EMPTY_STRING:
                    _segs.add(seg)
                    _seg_freqs[seg] += self._forms[form]
            ur += _abstractify(_segs, _seg_freqs)
        return ur

    def add_form(self, form):
        self.concrete = True
        if form not in self._forms:
            self.form = form
        self._forms[form] += 1
        # set form to most frequent form
        try:
            self.form = sorted(self._forms.items(), reverse=True, key=lambda it: (it[-1], f'{it[0]}'))[0][0]
        except TypeError as e:
            print(e)
            print(f'***** {self._forms} *****')

        n = sum(self._forms.values())
        assert(n >= 1)
        e = n - self._forms[self.form] # count occurances in form other than most frequent
        theta_n = np.log(n)
        if e > n / theta_n if theta_n > 0 else False: # keep concrete form and lexicalize exceptions                        
            abstract_form = self.collapse_into_abstract()
            if abstract_form:
                self.form = abstract_form
                self.concrete = False
            else:
                print(f'Unable to form abstract UR for {self.feat} with forms {self._forms}')

        if self.form == '':
            self.null = True
