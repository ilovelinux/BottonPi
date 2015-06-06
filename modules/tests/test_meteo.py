import unittest
import sys
sys.path += ['/home/pi/.irc3/modules/']
import meteo

class OpenWeatherMapTest(unittest.TestCase):
    def test_openweathermap(self):
        self.assertIn('Rome', meteo.cmd_opm({'<city>':['Rome']}))
    def test_openweathermap_space(self):
        self.assertIn('New York', meteo.cmd_opm({'<city>':['New', 'York']}))
    def test_openweathermap_no_result(self):
        self.assertEqual('Nessun risultato per "*"', meteo.cmd_opm({'<city>':['*']}))

class YahooWeatherTest(unittest.TestCase):
    def test_yahooweather(self):
        self.assertIn('Rome', meteo.cmd_ym({'<city>':['Rome']}))
    def test_yahooweather_space(self):
        self.assertIn('New York', meteo.cmd_ym({'<city>':['New', 'York']}))
    def test_yahooweather_no_result(self):
        self.assertIn('Nessun risultato per "*"', meteo.cmd_ym({'<city>':['*']}))
