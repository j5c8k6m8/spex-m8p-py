import unittest
from spexm8p.builder import spex


class TestBuilder(unittest.TestCase):

    def test1(self):
        self.assertEqual(spex('a'), spex('!([^a]|..+)'))

    def test2(self):
        self.assertEqual(spex('a+'), spex('!([^a]|.+[^a]|[^a].+|.+[^a].+)'))

    def test3(self):
        self.assertEqual(spex('ab'), spex('!(.|[^a].|.[^b]|...+)'))

    def test4(self):
        self.assertEqual(spex('(a+|ab)&!a'), spex('a(a+|b)'))

    def test5(self):
        self.assertTrue(spex('(a+|ab)&!a').include(spex('a(a+|b)')))

    def test6(self):
        self.assertTrue(spex('(a+|ab)').include(spex('a(a+|b)')))
