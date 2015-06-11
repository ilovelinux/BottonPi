import unittest
from modules import meteo

class OpenWeatherMapTest(unittest.TestCase):
    def test_openweathermap(self):
        self.assertIn('Rome',
                      meteo.cmd_opm({'<city>':['Rome']}))
    def test_openweathermap_space(self):
        self.assertIn('New York',
                      meteo.cmd_opm({'<city>':['New', 'York']}))
    def test_openweathermap_no_result(self):
        self.assertEqual('No results for "*"',
                         meteo.cmd_opm({'<city>':['*']}))
    def test_openweathermap_no_result_it(self):
        self.assertEqual('Nessun risultato per "*"',
                         meteo.cmd_opm({'<city>':['*']}, 'it'))

class YahooWeatherTest(unittest.TestCase):
    def test_yahooweather(self):
        self.assertIn('Rome', 
                      meteo.cmd_ym({'<city>':['Rome']}))
    def test_yahooweather_space(self):
        self.assertIn('New York',
                      meteo.cmd_ym({'<city>':['New', 'York']}))
    def test_yahooweather_no_result(self):
        self.assertEqual('No results for "*"',
                         meteo.cmd_ym({'<city>':['*']}))
    def test_yahooweather_no_result_it(self):
        self.assertEqual('Nessun risultato per "*"',
                         meteo.cmd_ym({'<city>':['*']}, 'it'))
