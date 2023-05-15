from form import Form
from morpheme import Morpheme
from alphabet import Alphabet
from utils import EMPTY_STRING

class Lexicon:
    def __init__(self, ipa_file, add_segs=True):
        self.alphabet = Alphabet(ipa_file=ipa_file, add_segs=add_segs)
        self.forms = dict()
        self.morphemes = dict()
        self.stems = set()
        self.affixes = set()
        
    def __len__(self):
        return len(self.forms)

    def __iter__(self):
        return sorted(self.morphemes.keys()).__iter__()

    def __contains__(self, key):
        '''
        :key: a Morpheme object
        '''
        if type(key) is Form:
            return key in self.forms
        if type(key) is Morpheme:
            return key in self.morphemes
        if type(key) is str and key in self.morphemes:
            return key in self.morphemes
        return False

    def __getitem__(self, key):
        try:
            if type(key) is Form:
                return self.forms[key]
            if type(key) is Morpheme:
                return self.morphemes[key]
            if type(key) is str and key in self.morphemes:
                return self.morphemes[key]
            raise KeyError(f'KeyError: {key} not in the Lexicon.')
        except KeyError as e:
            raise KeyError(f'KeyError: {key} not in the Lexicon.')

    def add_form(self, form, segmentation, analysis):
        form = Form(form=form, 
                    segmentation=segmentation, 
                    analysis=analysis, 
                    alphabet=self.alphabet)
                    
        if form not in self.forms:
            self.forms[form] = form
            # add morphemes
            if form.is_stem:
                self.add_morpheme(Morpheme(form.form))
            else:
                for s, a in form.parts():
                    self.add_morpheme(Morpheme(form=s, feat=a))

        return form
    
    def add_morpheme(self, morph):
        if morph not in self.morphemes:
            self.morphemes[morph] = morph
            if morph.is_stem:
                self.stems.add(morph)
            else:
                self.affixes.add(morph)
        else:
            self.morphemes[morph].add_form(morph.form)

    def build_train(self):
        train = set()
        for form in self.forms:
            ur, sr = self.build_ur_sr(form)
            train.add((ur, sr))
        return sorted(train)

    def build_ur_sr(self, form, segmentation=None, analysis=None, unknown=False, del_as_char=True, segmented=False):
        '''
        :unknown: if False (default), then require each morpheme to be in the lexicon
        '''
        if not unknown and form not in self:
            raise ValueError(':form: parameter must be in Lexicon')
        if not unknown and type(form) is not Form:
            raise ValueError(':form: parameter must be of type Form')
        form = self[form] if not unknown else Form(form=form, segmentation=segmentation, analysis=analysis, alphabet=self.alphabet)
        ur = '' if not segmented else list()
        sr = '' if not segmented else list()
        for s, a in form.parts(): # iterate over morphemes
            if a == 'Stem':
                ur += f'{s}' if not segmented else [f'{s}']
                sr += f'{s}' if not segmented else [f'{s}']
            else: # affix
                assert(type(a) is str) # analysis should be a string

                affix_sr = f'{s}'
                if a in self: # morpheme is in the lexicon
                    morph = self[a]
                    affix_ur = affix_sr if form in self and morph.concrete else f'{morph.form}'
                    if del_as_char and not morph.concrete:
                        while len(affix_sr) < len(affix_ur): # DELETION
                            affix_sr = EMPTY_STRING + affix_sr
                        while len(affix_sr) > len(affix_ur): # EPENTHESIS
                            affix_ur = EMPTY_STRING + affix_ur
                else: # morepheme not in the lexicon
                    if not unknown:
                        raise KeyError(f'Morpheme {a} not in lexicon. Set :unknown: to True to replace with "?"\'s')
                    affix_ur = '?' * len(s)
                sr += affix_sr if not segmented else [affix_sr]
                ur += affix_ur if not segmented else [affix_ur]
        return (ur, sr) if not segmented else ('-'.join(ur), '-'.join(sr))