# Towards a Learning-Based Account of Underlying Forms: A Case-Study in Turkish
This repository provides code for 2023 SCiL paper "Towards a Learning-Based Account of Underlying Forms: A Case-Study in Turkish"

```bibtex
@article{belth2023urs,
  title={Towards a Learning-Based Account of Underlying Forms: A Case-Study in Turkish},
  author={Belth, Caleb},
  journal={Proceedings of the Society for Computation in Linguistics},
  year={2023}
}
```

## Running Code

This assumes that you are running from the `src/` directory.

We start by importing the `Lexicon` class.

```python
from lexicon import Lexicon
```

We can create a lexicon object, and point it to an ipa file in order to interpret segments as feature sets.

```python
>>> lexicon = Lexicon(ipa_file='../data/ipa.txt')
```

```python
>>> from lexicon import Lexicon
```

If we add the first three words from Table 1 in the paper, the UR for the plural affix is the concrete /-lɑr/.

```python
>>> lexicon.add_form(form='buzlɑr', segmentation='buz-lɑr', analysis='Stem-pl')
>>> lexicon.add_form(form='kɯzlɑr', segmentation='kɯz-lɑr', analysis='Stem-pl')
>>> lexicon.add_form(form='eller', segmentation='el-ler', analysis='Stem-pl')
>>> print(lexicon['pl'])
-lɑr
```

However, if we continue to add the remaning nine words, the surface alternation of the plural affix leads the model to construct the abstract UR /-lAr/. The genetive affix is thus far the concrete /-in/.

```python
>>> lexicon.add_form(form='jerlerin', segmentation='jer-ler-in', analysis='Stem-pl-gen')
>>> lexicon.add_form(form='søzler', segmentation='søz-ler', analysis='Stem-pl')
>>> lexicon.add_form(form='dɑllɑrɯn', segmentation='dɑl-lɑr-ɯn', analysis='Stem-pl-gen')
>>> lexicon.add_form(form='sɑplɑr', segmentation='sɑp-lɑr', analysis='Stem-pl')
>>> lexicon.add_form(form='jyzyn', segmentation='jyz-yn', analysis='Stem-gen')
>>> lexicon.add_form(form='iplerin', segmentation='ip-ler-in', analysis='Stem-pl-gen')
>>> print(lexicon['pl'])
-lAr
>>> print(lexicon['gen'])
-in
```

## Learning Alternations

The model from Belth (2023a) is not yet publically available. When that changes, we will update this repository to include that code.