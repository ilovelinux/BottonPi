import unittest
from modules import utility

class RandomTest(unittest.TestCase):
    def test_random(self):
        test = utility.rand(args={'<parole>':['Pippo', 'Pluto']})
        self.assertIn(test, ['Random <Pippo, Pluto>: Pippo', 
                             'Random <Pippo, Pluto>: Pluto'])
    def test_random_one_word(self):
        test = utility.rand(args={'<parole>':['Pippo']})
        self.assertEqual(test, 'Inserire due o più parole')

class LeetTest(unittest.TestCase):
    def test_leet(self):
        test = utility.leet(args={'<parole>':['test']})
        self.assertEqual(test, 'Leet <test>: 7357')

class SourceTest(unittest.TestCase):
    def test_source(self):
        test = utility.source()
        self.assertEqual(test, 'https://bitbucket.org/ilovelinux/bottonpi/src')

class CountdownTest(unittest.TestCase):
    def test_countdown(self):
        test = utility.countdown(args={'<secs>':['10']})
        self.assertEqual(test, 'Conto alla rovescia terminato')

class UptimeTest(unittest.TestCase):
    def test_uptime(self):
        test = utility.uptime()
        self.assertIn('Uptime: ', test)

class ReverseTest(unittest.TestCase):
    def test_reverse(self):
        test = utility.reverse(args={'<rev>':['test']})
        self.assertEqual(test, 'Reverse <test>: tset')

class LenTest(unittest.TestCase):
    def test_len(self):
        test = utility.len(args={'<text>':['test']})
        self.assertEqual(test, 'Lenght <test>: 4')
