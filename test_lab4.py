from unittest import TestCase, main

from relation import make_relations
from parse import parse
from set_grammar import all_tokens, constants, variables, precedence, prefix


class ParserTest(TestCase):
    def setUp(self):
        self.relations = make_relations(all_tokens, variables, constants, prefix, precedence)

    def test1(self):
        tokens = "- ( not 1 )".split()
        parse_res = parse(tokens, all_tokens, self.relations)
        self.assertEqual(parse_res.result, "1 not -")

    def test2(self):
        tokens = "a b c".split()
        parse_res = parse(tokens, all_tokens, self.relations)
        self.assertEqual(parse_res.is_correct, False)

    def test3(self):
        tokens = "( ( ( a / b ) ) )".split()
        parse_res = parse(tokens, all_tokens, self.relations)
        self.assertEqual(parse_res.result, "a b /")

    def test4(self):
        tokens = "( a mod b ) or c".split()
        parse_res = parse(tokens, all_tokens, self.relations)
        self.assertEqual(parse_res.result, "a b mod c or")
    
    def test5(self):
        tokens = "( a mod b ) and c * C <> not a".split()
        parse_res = parse(tokens, all_tokens, self.relations)
        self.assertEqual(parse_res.result, "a b mod c and C * a not <>")



if __name__ == "__main__":
    main()