import unittest
from solver import StringReader, Lexer, Parser, SYMBOLS, Variable


class TestLexer(unittest.TestCase):

    def test_test(self):
        lx = Lexer("2 + sinx + 3 * 44.0 * a + sin * ln + inf * pi")
        tokens = lx.get_tokens()

class TestReader(unittest.TestCase):

    def test_pos(self):
        reader = StringReader("test")
        self.assertEqual(reader.pos, 0)
        reader.read(2)
        self.assertEqual(reader.pos, 2)

    def test_set_pos(self):
        reader = StringReader("test")
        reader.next()
        self.assertEqual(reader.pos, 1)
        reader.pos = 0
        self.assertEqual(reader.pos, 0)
        reader.pos = 3
        self.assertEqual(reader.pos, 3)
        self.assertEqual(reader.next(), "t")

    def test_length(self):
        reader = StringReader("test")
        self.assertEqual(reader.length, 4)

    def test_peak(self):
        reader = StringReader("Anders er kul")
        self.assertEqual(reader.peak(), "A")
        self.assertEqual(reader.peak(), "A")

    def test_peak_n(self):
        reader = StringReader("Anders er kul")
        self.assertEqual(reader.peak(), "A")
        self.assertEqual(reader.peak(3), "And")

    def test_next(self):
        reader = StringReader("Anders er kul")
        self.assertEqual(reader.next(), "A")
        self.assertEqual(reader.next(), "n")

    def test_read(self):
        reader = StringReader("Anders er kul")
        self.assertEqual(reader.read(5), "Ander")

    def test_read_full(self):
        reader = StringReader("Anders er kul")
        self.assertEqual(reader.read(reader.length), "Anders er kul")

    def test_read_until(self):
        reader = StringReader("Anders er kul")
        reader.next()
        self.assertEqual(reader.read_until("k"), "nders er k")
        self.assertEqual(reader.next(), "u")

    def test_read_until(self):
        reader = StringReader("Anders er kul")
        reader.next()
        self.assertEqual(reader.read_until("x"), "nders er kul")

    def test_skip_whitespace(self):
        reader = StringReader("a   b c  d")
        self.assertEqual(reader.next(), "a")
        reader.skip_whitespace()
        self.assertEqual(reader.next(), "b")
        reader.skip_whitespace()
        self.assertEqual(reader.next(), "c")
        reader.skip_whitespace()
        self.assertEqual(reader.next(), "d")

    def test_raise_next(self):
        reader = StringReader("a")
        self.assertEqual(reader.next(), "a")
        self.assertRaises(IndexError, reader.next)

    def test_raise_peak(self):
        reader = StringReader("a")
        self.assertEqual(reader.next(), "a")
        self.assertRaises(IndexError, reader.peak)

    def test_raise_read(self):
        reader = StringReader("a")
        self.assertRaises(IndexError, reader.read, 2)

    def test_raise_read_until(self):
        reader = StringReader("Anders er kul")
        self.assertRaises(AttributeError, reader.read_until, "dd")

    def test_raise_set_pos(self):
        reader = StringReader("test")
        def set_pos():
            reader.pos = 4
        self.assertRaises(IndexError, set_pos)


if __name__ == "__main__":
    unittest.main()
