import unittest
from spexm8p.parser import parse, tokenize


class TestParse(unittest.TestCase):

    def test_tokenize_normal(self):
        self.maxDiff = None
        tokens = tokenize('abc')
        self.assertEqual(parse(tokens), {'type': 'concat', 'nodes': [
            {'type': 'inc_chex', 'tokens': ['a']},
            {'type': 'inc_chex', 'tokens': ['b']},
            {'type': 'inc_chex', 'tokens': ['c']},
        ]})

    def test_tokenize_normal1(self):
        self.maxDiff = None
        tokens = tokenize('ab(cd)')
        self.assertEqual(parse(tokens), {'type': 'concat', 'nodes': [
            {'type': 'inc_chex', 'tokens': ['a']},
            {'type': 'inc_chex', 'tokens': ['b']},
            {'type': 'concat', 'nodes': [
                {'type': 'inc_chex', 'tokens': ['c']},
                {'type': 'inc_chex', 'tokens': ['d']},
            ]},
        ]})

    def test_tokenize_normal2(self):
        self.maxDiff = None
        tokens = tokenize('ab(cd(ef))gh')
        self.assertEqual(parse(tokens), {'type': 'concat', 'nodes': [
            {'type': 'inc_chex', 'tokens': ['a']},
            {'type': 'inc_chex', 'tokens': ['b']},
            {'type': 'concat', 'nodes': [
                {'type': 'inc_chex', 'tokens': ['c']},
                {'type': 'inc_chex', 'tokens': ['d']},
                {'type': 'concat', 'nodes': [
                    {'type': 'inc_chex', 'tokens': ['e']},
                    {'type': 'inc_chex', 'tokens': ['f']},
                ]},
            ]},
            {'type': 'inc_chex', 'tokens': ['g']},
            {'type': 'inc_chex', 'tokens': ['h']},
        ]})

    def test_tokenize_wildchar(self):
        self.maxDiff = None
        tokens = tokenize('.')
        self.assertEqual(parse(tokens), {
            'type': 'exc_chex',
            'tokens': []
        })

    def test_tokenize_wildchar2(self):
        self.maxDiff = None
        tokens = tokenize('[^.]')
        self.assertEqual(parse(tokens), {
            'type': 'inc_chex',
            'tokens': []
        })

    def test_tokenize_chex(self):
        self.maxDiff = None
        tokens = tokenize('[abc][^abc]')
        self.assertEqual(parse(tokens), {'type': 'concat', 'nodes': [
            {'type': 'inc_chex', 'tokens': ['a', 'b', 'c']},
            {'type': 'exc_chex', 'tokens': ['a', 'b', 'c']},
        ]})

    def test_invert(self):
        self.maxDiff = None
        tokens = tokenize('![abc]')
        self.assertEqual(parse(tokens), {
            'type': 'invert',
            'node': {'type': 'inc_chex', 'tokens': ['a', 'b', 'c']}
        })

    def test_invert2(self):
        self.maxDiff = None
        tokens = tokenize('!a+')
        self.assertEqual(parse(tokens), {
            'type': 'invert',
            'node': {
                'type': 'repeat',
                'node': { 'type': 'inc_chex', 'tokens': ['a'], }
            },
        })

    def test_and(self):
        self.maxDiff = None
        tokens = tokenize('[abc]&[bcd]')
        self.assertEqual(parse(tokens), {
            'type': 'and',
            'left': {'type': 'inc_chex', 'tokens': ['a', 'b', 'c']},
            'right': {'type': 'inc_chex', 'tokens': ['b', 'c', 'd']},
        })

    def test_or(self):
        self.maxDiff = None
        tokens = tokenize('[abc]|[bcd]')
        self.assertEqual(parse(tokens), {
            'type': 'or',
            'left': {'type': 'inc_chex', 'tokens': ['a', 'b', 'c']},
            'right': {'type': 'inc_chex', 'tokens': ['b', 'c', 'd']},
        })


if __name__ == '__main__':
    unittest.main()
