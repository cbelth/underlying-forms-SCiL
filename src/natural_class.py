from utils import PRIMARY_STRESS, SECONDARY_STRESS, SYLLABLE_BOUNDARY, LEFT_WORD_BOUNDARY, RIGHT_WORD_BOUNDARY

class NaturalClass:
    def __init__(self, feats, alphabet, params=None):
        self._wildcard = feats == '*'
        self.feats = set(feats)
        self.alphabet = alphabet
        self.params = params
        self._update()

    def segments(self):
        segs = set()
        for seg in self.alphabet.segments:
            if seg == '_':
                continue
            if seg in self:
                segs.add(seg)
        return segs

    def _update(self):
        self.name = '{' + ','.join(sorted(self.feats)) + '}'
        self.extension_str = '{' + ','.join(sorted(f'{seg}' for seg in self.alphabet.extension(self))) + '}'

    def add_feat(self, feat):
        self.feats.add(feat)
        self._update()

    def remove_feat(self, feat):
        self.feats.discard(feat)
        self._update()

    def intersection(self, other):
        if type(other) is not set:
            raise TypeError('Cannot intersection NaturalClass with something other than a set.') 
        return set(filter(lambda seg: seg in self, other))

    def __str__(self):
        return self.name if self.params is None or self.params.NC_AS_FEATURES else self.extension_str

    def __repr__(self):
        return self.__str__()

    def __contains__(self, item):
        if self._wildcard:
            return True
        if item in {SYLLABLE_BOUNDARY, LEFT_WORD_BOUNDARY, RIGHT_WORD_BOUNDARY}:
            return False
        if len(item) > 1 and item[-1] not in {PRIMARY_STRESS, SECONDARY_STRESS}:
            return False
        return self.alphabet.feat_vals(f'{item}').intersection(self.feats) == self.feats

    def __len__(self):
        return len(self.feats)

    def __eq__(self, other):
        if type(other) is set:
            return self.alphabet.extension(self) == other
        return self.feats == other.feats

    def copy(self):
        return NaturalClass(self.feats, self.alphabet, self.params)