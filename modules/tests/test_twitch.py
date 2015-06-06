import unittest
from modules import twitch

class Twitch(unittest.TestCase):
    def test_twitch_not_found(self):
        self.assertEqual('Il canale "*" non è stato trovato', twitch.twitch(args = {'<channel>':['*']}))
