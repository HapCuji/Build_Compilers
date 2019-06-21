from unittest import TestCase, main

from parser import Parser


class ParserTest(TestCase):

    def test1(self):
        p = Parser("not(A+B)*1 = not B mod (2 and D)")
        self.assertEqual(True, p.accept_string())

    def test2(self):
        p = Parser("not not B")
        self.assertEqual(True, p.accept_string())

    def test3(self):
        p = Parser(" A ~ C")
        self.assertEqual(False, p.accept_string())

    def test4(self):
        p = Parser("A div mod C")
        self.assertEqual(False, p.accept_string())

    def test5(self):
        p = Parser("- ( not 5)")
        self.assertEqual(True, p.accept_string())
   
    def test6(self):
        p = Parser("- not B")
        self.assertEqual(True, p.accept_string())

    def test7(self):
        p = Parser("( A mod B ) and B * C <> not A")
        self.assertEqual(True, p.accept_string())

    def test8(self):
        p = Parser("- (+ not 5 G)")
        self.assertEqual(False, p.accept_string())
   
    

if __name__ == "__main__":
    main()