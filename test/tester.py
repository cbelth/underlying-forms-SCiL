import unittest
from test_utils import TestUtils
from test_segment import TestSegment
from test_sequence import TestSequence
from test_alphabet import TestAlphabet
from test_morpheme import TestMorpheme

'''
A script to run all the test cases.
'''

def build_suite(klass):
    return unittest.TestLoader().loadTestsFromTestCase(klass)

# combine the test suites
suites = unittest.TestSuite([build_suite(TestUtils),
                             build_suite(TestSegment),
                             build_suite(TestSequence),
                             build_suite(TestAlphabet),
                             build_suite(TestMorpheme)])
# run the test suites
unittest.TextTestRunner(verbosity=2).run(suites)
