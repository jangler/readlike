import unittest

import readlike as rl


class TestReadlike(unittest.TestCase):
    def test_backward_char(self):
        self.assertEqual(rl._backward_char('', 0), ('', 0))
        self.assertEqual(rl._backward_char('test', 0), ('test', 0))
        self.assertEqual(rl._backward_char('test', 1), ('test', 0))
        self.assertEqual(rl._backward_char('test', 4), ('test', 3))

    def test_backward_delete_char(self):
        self.assertEqual(rl._backward_delete_char('', 0), ('', 0))
        self.assertEqual(rl._backward_delete_char('test', 0), ('test', 0))
        self.assertEqual(rl._backward_delete_char('test', 1), ('est', 0))
        self.assertEqual(rl._backward_delete_char('test', 4), ('tes', 3))

    def test_backward_kill_word(self):
        self.assertEqual(rl._backward_kill_word('', 0), ('', 0))
        self.assertEqual(rl._backward_kill_word('test', 0), ('test', 0))
        self.assertEqual(rl._backward_kill_word('test', 2), ('st', 0))
        self.assertEqual(rl._backward_kill_word('hi. yo. ', 4), ('yo. ', 0))
        self.assertEqual(rl._backward_kill_word('hi. yo. ', 5), ('hi. o. ', 4))
        self.assertEqual(rl._backward_kill_word('hi. yo. ', 8), ('hi. ', 4))

    def test_backward_word(self):
        self.assertEqual(rl._backward_word('', 0), ('', 0))
        self.assertEqual(rl._backward_word('test', 0), ('test', 0))
        self.assertEqual(rl._backward_word('hi. yo. ', 3), ('hi. yo. ', 0))
        self.assertEqual(rl._backward_word('hi. yo. ', 4), ('hi. yo. ', 0))
        self.assertEqual(rl._backward_word('hi. yo. ', 5), ('hi. yo. ', 4))
        self.assertEqual(rl._backward_word('hi. yo. ', 8), ('hi. yo. ', 4))

    def test_beginning_of_line(self):
        self.assertEqual(rl._beginning_of_line('', 0), ('', 0))
        self.assertEqual(rl._beginning_of_line('test', 0), ('test', 0))
        self.assertEqual(rl._beginning_of_line('test', 4), ('test', 0))

    def test_capitalize_word(self):
        self.assertEqual(rl._capitalize_word('', 0), ('', 0))
        self.assertEqual(rl._capitalize_word('test', 0), ('Test', 4))
        self.assertEqual(rl._capitalize_word('test', 3), ('tesT', 4))
        self.assertEqual(rl._capitalize_word('test', 4), ('test', 4))
        self.assertEqual(rl._capitalize_word('. test', 0), ('. Test', 6))
        self.assertEqual(rl._capitalize_word('test  ', 1), ('tEst  ', 4))

    def test_delete_char(self):
        self.assertEqual(rl._delete_char('', 0), ('', 0))
        self.assertEqual(rl._delete_char('test', 0), ('est', 0))
        self.assertEqual(rl._delete_char('test', 4), ('test', 4))

    def test_delete_horizontal_space(self):
        self.assertEqual(rl._delete_horizontal_space('', 0), ('', 0))
        self.assertEqual(rl._delete_horizontal_space('hi', 1), ('hi', 1))
        self.assertEqual(rl._delete_horizontal_space(' hi ', 2), (' hi ', 2))
        self.assertEqual(rl._delete_horizontal_space('\t \t', 1), ('', 0))
        self.assertEqual(rl._delete_horizontal_space('.  .', 2), ('..', 1))

    def test_downcase_word(self):
        self.assertEqual(rl._downcase_word('', 0), ('', 0))
        self.assertEqual(rl._downcase_word('TEST', 0), ('test', 4))
        self.assertEqual(rl._downcase_word('TEST', 2), ('TEst', 4))
        self.assertEqual(rl._downcase_word('TEST', 4), ('TEST', 4))
        self.assertEqual(rl._downcase_word('. TEST', 0), ('. test', 6))
        self.assertEqual(rl._downcase_word('TEST  ', 1), ('Test  ', 4))

    def test_forward_char(self):
        self.assertEqual(rl._forward_char('', 0), ('', 0))
        self.assertEqual(rl._forward_char('test', 0), ('test', 1))
        self.assertEqual(rl._forward_char('test', 4), ('test', 4))

    def test_forward_word(self):
        self.assertEqual(rl._forward_word('', 0), ('', 0))
        self.assertEqual(rl._forward_word('test', 4), ('test', 4))
        self.assertEqual(rl._forward_word('hi yo ', 1), ('hi yo ', 2))
        self.assertEqual(rl._forward_word('hi yo ', 3), ('hi yo ', 5))
        self.assertEqual(rl._forward_word('hi yo ', 5), ('hi yo ', 6))

    def test_kill_line(self):
        self.assertEqual(rl._kill_line('', 0), ('', 0))
        self.assertEqual(rl._kill_line('test', 0), ('', 0))
        self.assertEqual(rl._kill_line('test', 2), ('te', 2))
        self.assertEqual(rl._kill_line('test', 4), ('test', 4))

    def test_kill_word(self):
        self.assertEqual(rl._kill_word('', 0), ('', 0))
        self.assertEqual(rl._kill_word('test', 4), ('test', 4))
        self.assertEqual(rl._kill_word('hi yo ', 1), ('h yo ', 1))
        self.assertEqual(rl._kill_word('hi yo ', 3), ('hi  ', 3))
        self.assertEqual(rl._kill_word('hi yo ', 5), ('hi yo', 5))

    def test_transpose_chars(self):
        self.assertEqual(rl._transpose_chars('', 0), ('', 0))
        self.assertEqual(rl._transpose_chars('test', 0), ('test', 0))
        self.assertEqual(rl._transpose_chars('test', 2), ('tset', 3))
        self.assertEqual(rl._transpose_chars('test', 4), ('tets', 4))

    def test_transpose_words(self):
        self.assertEqual(rl._transpose_words('', 0), ('', 0))
        self.assertEqual(rl._transpose_words('test', 2), ('test', 2))
        self.assertEqual(rl._transpose_words('ab cd ef', 1), ('ab cd ef', 1))
        self.assertEqual(rl._transpose_words('ab cd ef', 2), ('cd ab ef', 5))
        self.assertEqual(rl._transpose_words('ab cd ef', 4), ('cd ab ef', 5))
        self.assertEqual(rl._transpose_words('ab cd ef', 5), ('ab ef cd', 8))
        self.assertEqual(rl._transpose_words('ab cd ef', 8), ('ab ef cd', 8))
        self.assertEqual(rl._transpose_words('ab,./cd', 2), ('cd,./ab', 7))

    def test_unix_line_discard(self):
        self.assertEqual(rl._unix_line_discard('', 0), ('', 0))
        self.assertEqual(rl._unix_line_discard('test', 0), ('test', 0))
        self.assertEqual(rl._unix_line_discard('test', 2), ('st', 0))
        self.assertEqual(rl._unix_line_discard('test', 4), ('', 0))

    def test_unix_word_rubout(self):
        self.assertEqual(rl._unix_word_rubout('', 0), ('', 0))
        self.assertEqual(rl._unix_word_rubout('test', 0), ('test', 0))
        self.assertEqual(rl._unix_word_rubout('hi  yo  ', 3), (' yo  ', 0))
        self.assertEqual(rl._unix_word_rubout('hi  yo  ', 4), ('yo  ', 0))
        self.assertEqual(rl._unix_word_rubout('hi  yo  ', 5), ('hi  o  ', 4))
        self.assertEqual(rl._unix_word_rubout('hi  yo  ', 8), ('hi  ', 4))

    def test_upcase_word(self):
        self.assertEqual(rl._upcase_word('', 0), ('', 0))
        self.assertEqual(rl._upcase_word('test', 0), ('TEST', 4))
        self.assertEqual(rl._upcase_word('test', 2), ('teST', 4))
        self.assertEqual(rl._upcase_word('test', 4), ('test', 4))
        self.assertEqual(rl._upcase_word('. test', 0), ('. TEST', 6))
        self.assertEqual(rl._upcase_word('test  ', 1), ('tEST  ', 4))

    def test_edit(self):
        self.assertEqual(rl.edit('test', 4, 's'), ('tests', 5))
        self.assertEqual(rl.edit('test', 4, 'ctrl h'), ('tes', 3))
        self.assertEqual(rl.edit('test', 4, 'bogus'), ('test', 4))

    def test_keys(self):
        self.assertEqual(type(rl.keys()), type(frozenset()))
        self.assertNotEqual(len(rl.keys()), 0)


if __name__ == '__main__':
    unittest.main()
