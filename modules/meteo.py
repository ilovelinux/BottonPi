# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import urllib.request
import json
import feedparser

@command
def meteo(self, mask, target, args):
    """Indica il meteo della città

        %%meteo <city>...
    """
    openweather = 'OpenWeatherMap: {}'.format(cmd_opm(args))
    yahooweath = 'Yahoo Weather: {}'.format(cmd_ym(args))
    return [openweather, yahooweath]

@command
def weather(self, mask, target, args):
    """Indica il meteo della città

        %%weather <city>...
    """
    return ['OpenWeatherMap: {}'.format(cmd_opm(args)),'Yahoo Weather: {}'.format(cmd_ym(args))]

@command
def opm(self, mask, target, args):
    """Meteo OpenWeatherMap

        %%opm <city>...
    """
    return cmd_opm(args)

@command
def openweathermap(self, mask, target, args):
    """Meteo OpenWeatherMap

        %%openweathermap <city>...
    """
    return cmd_opm(args)

@command
def ym(self, mask, target, args):
    """Meteo yahoo

        %%ym <city>...
    """
    return cmd_ym(args)
    
@command
def yahooweather(self, mask, target, args):
    """Meteo yahoo

        %%yahooweather <city>...
    """
    return cmd_ym(args)

def cmd_opm(args):
    city = ' '.join(args['<city>'])
    city1 = city.replace(' ', '_')
    url = 'http://api.openweathermap.org/data/2.5/weather?lang=it&units=metric&q='
    try:
        a = urllib.request.urlopen(url + str(city1), data=None).read()
    except:
        return 'Impossibile connettersi al momento'
    results = json.loads(a.decode('utf8'))
    if results == {'cod': '404', 'message': 'Error: Not found city'}:
        return 'Nessun risultato per "{}"'.format(city)
    citta = '{}, {}'.format(results['name'], results['sys']['country'])
    longitudine = '{}'.format(results['coord']['lon'])
    latitudine = '{}'.format(results['coord']['lat'])
    vento = '{}'.format(results['wind']['speed'])
    umidita = '{}'.format(results['main']['humidity'])
    nuvolosita = '{}'.format(results['clouds']['all'])
    temperatura = '{}'.format(results['main']['temp'])
    temperaturamin = '{}'.format(results['main']['temp_min'])
    temperaturamax = '{}'.format(results['main']['temp_max'])
    stato = '{}'.format(results['weather'][0]['description'])
    if temperatura == temperaturamin == temperaturamax:
        status = ["Citta': {}".format(citta),
                  "Temperatura: {}°C".format(temperatura),
                  "Umidita': {}%".format(umidita),
                  "Nuvolosita': {}%".format(nuvolosita),
                  "Vento: {} km/h - {}".format(vento, stato)]
    else:
        status = ["Citta': {}".format(citta),
                  "Temperatura: {}°C (Max: {}°C, Min:{}°C)".format(temperatura, temperaturamax, temperaturamin),
                  "Umidita': {}%".format(umidita),
                  "Nuvolosita': {}%".format(nuvolosita),
                  "Vento: {} km/h - Stato: {}".format(vento, stato)]
    return ' · '.join(status)

def cmd_ym(args):
    city = ' '.join(args['<city>'])
    city1 = city.replace(' ', '_')
    url = 'http://weather.yahooapis.com/forecastrss?u=c&q='
    open = urllib.request.urlopen('{}{}'.format(url, city1))
    results = feedparser.parse(open)
    città = '{}, {}'.format(results['feed']['yweather_location']['city'], results['feed']['yweather_location']['country'])
    speed = float(results['feed']['yweather_wind']['speed'])
    vento = '{} {}'.format(speed, results['feed']['yweather_units']['speed'])
    umidità = '{}%'.format(results['feed']['yweather_atmosphere']['humidity'])
    if results['feed']['yweather_atmosphere']['visibility']:
        visibilità = '{} {}'.format(results['feed']['yweather_atmosphere']['visibility'], results['feed']['yweather_units']['distance'])
    else:
        visibilità = 'Non disponibile'
    temperatura = results.entries[0]['yweather_condition']['temp']
    if speed < 1:
        description = 'Calmo'
    elif speed < 4:
        description = 'Aria leggera'
    elif speed < 7:
        description = 'Brezza leggera'
    elif speed < 11:
        description = 'Brezza gentile'
    elif speed < 16:
        description = 'Brezza moderata'
    elif speed < 22:
        description = 'Brezza fresca'
    elif speed < 28:
        description = 'Forte vento'
    elif speed < 34:
        description = 'Nei pressi di una burrasca'
    elif speed < 41:
        description = 'Burrasca'
    elif speed < 48:
        description = 'Nei pressi di un temporale'
    elif speed < 56:
        description = 'Temporale'
    elif speed < 64:
        description = 'Temporale violento'
    else:
        description = 'Uragano'
    status = ['Città: {}'.format(città),
              'Temperatura: {}°C'.format(temperatura),
              'Umidità: {}'.format(umidità),
              'Visibilità: {}'.format(visibilità),
              'Vento: {} - {}'.format(vento, description)]
    return ' · '.join(status)
