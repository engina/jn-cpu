import unittest
import utils
import sys

class TestTokenizer(unittest.TestCase):
    str1 = """
"hello" world what's up
"""
    str2 = "    MOV X, 0x5000\n"

    str3 = """
  two empty spaces and some escaped chars \\"\\' in normal textfollowed by a "dbl quote" and then a 'single quote'
wait there is more!! "'signle quotes' inside a double quote" and '"double quotes" inside a single quote'
wait! there\\'s more!! "escaped double quotes \\" and escaped single quotes\\' " """
    # join back together a tokenized string
    def join(self, tokens):
        t = []
        for token in tokens:
            t.append(token['token'])
        return ''.join(t)

    def testTokens(self):
        tokens = utils.tokenize(self.str3)
        self.assertEqual(11, len(tokens))
        self.assertEqual('\n  two empty spaces and some escaped chars \\\"\\\' in normal textfollowed by a ', tokens[0]['token'])
        self.assertEqual('"dbl quote"', tokens[1]['token'])
        self.assertEqual(' and then a ', tokens[2]['token'])
        self.assertEqual("'single quote'", tokens[3]['token'])
        self.assertEqual('\nwait there is more!! ', tokens[4]['token'])
        self.assertEqual('"\'signle quotes\' inside a double quote"', tokens[5]['token'])
        self.assertEqual(' and ', tokens[6]['token'])
        self.assertEqual('\'"double quotes" inside a single quote\'', tokens[7]['token'])
        self.assertEqual('\nwait! there\\\'s more!! ', tokens[8]['token'])
        self.assertEqual('"escaped double quotes \\" and escaped single quotes\\\' "', tokens[9]['token'])
        self.assertEqual(' ', tokens[10]['token'])
        self.assertEqual(utils.TOKEN_NORMAL, tokens[0]['type'])
        self.assertEqual(utils.TOKEN_DBL_Q, tokens[1]['type'])
        self.assertEqual(utils.TOKEN_NORMAL, tokens[2]['type'])
        self.assertEqual(utils.TOKEN_SNG_Q, tokens[3]['type'])
        self.assertEqual(utils.TOKEN_NORMAL, tokens[4]['type'])
        self.assertEqual(utils.TOKEN_DBL_Q, tokens[5]['type'])
        self.assertEqual(utils.TOKEN_NORMAL, tokens[6]['type'])
        self.assertEqual(utils.TOKEN_SNG_Q, tokens[7]['type'])
        self.assertEqual(utils.TOKEN_NORMAL, tokens[8]['type'])
        self.assertEqual(utils.TOKEN_DBL_Q, tokens[9]['type'])
        self.assertEqual(utils.TOKEN_NORMAL, tokens[10]['type'])


    def testEquality(self):
        self.assertEqual(self.str1, self.join(utils.tokenize(self.str1)))
        self.assertEqual(self.str2, self.join(utils.tokenize(self.str2)))
        self.assertEqual(self.str3, self.join(utils.tokenize(self.str3)))
