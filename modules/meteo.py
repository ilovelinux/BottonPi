from irc3.plugins.command import command
import urllib.request
import json
import feedparser

@command
def meteo(self=None, mask=None, target=None, args=None):
    """Indicates the weather of the city

        %%meteo <city>...
    """
    return ['OpenWeatherMap: {}'.format(cmd_opm(args, lang='it')),
            'Yahoo Weather: {}'.format(cmd_ym(args, lang='it'))]

@command
def weather(self=None, mask=None, target=None, args=None):
    """Indicates the weather of the city

        %%weather <city>...
    """
    return ['OpenWeatherMap: {}'.format(cmd_opm(args)),
            'Yahoo Weather: {}'.format(cmd_ym(args))]

@command
def opm(self=None, mask=None, target=None, args=None):
    """OpenWeatherMap Weather

        %%opm <city>...
    """
    return cmd_opm(args)

@command
def opmit(self=None, mask=None, target=None, args=None):
    """Meteo di OpenWeatherMap

        %%opmit <city>...
    """
    return cmd_opm(args, lang='it')

@command
def openweathermap(self, mask, target, args):
    """OpenWeatherMap Weather

        %%openweathermap <city>...
    """
    return cmd_opm(args)

@command
def openweathermapit(self=None, mask=None, target=None, args=None):
    """Meteo di OpenWeatherMap

        %%openweathermapit <city>...
    """
    return cmd_opm(args, lang='it')
@command
def ym(self=None, mask=None, target=None, args=None):
    """yahoo Weather

        %%ym <city>...
    """
    return cmd_ym(args)

@command
def ymit(self=None, mask=None, target=None, args=None):
    """yahoo Weather

        %%ymit <city>...
    """
    return cmd_ym(args, lang='it')
    
@command
def yahooweather(self=None, mask=None, target=None, args=None):
    """Yahoo Weather

        %%yahooweather <city>...
    """
    return cmd_ym(args)

@command
def yahooweatherit(self=None, mask=None, target=None, args=None):
    """Yahoo Weather

        %%yahooweatherir <city>...
    """
    return cmd_ym(args, lang='it')

def cmd_opm(args, lang='en'):
    city = ' '.join(args['<city>'])
    api = 'http://api.openweathermap.org/data/2.5/weather'
    options = '?lang=it&units=metric&q='
    url = '{}{}{}'.format(api, options, city.replace(' ', '_'))
    try:
        page = urllib.request.urlopen(url).read()
    except:
        if lang == 'en':
            return 'Unable to connect at the time'
        if lang == 'it':
            return 'Impossibile connettersi al momento'
    results = json.loads(page.decode('utf8'))
    if results == {'cod': '404', 'message': 'Error: Not found city'}:
        if lang == 'en':
            return 'No results for "{}"'.format(city)
        if lang == 'it':
            return 'Nessun risultato per "{}"'.format(city)
    city = '{}, {}'.format(results['name'], results['sys']['country'])
#    longitude = '{}'.format(results['coord']['lon'])
#    latitude = '{}'.format(results['coord']['lat'])
    wind = results['wind']['speed']
    humidity = results['main']['humidity']
    clouds = results['clouds']['all']
    temp = '{}°C'.format(results['main']['temp'])
    mintemp = results['main']['temp_min']
    maxtemp = results['main']['temp_max']
    if temp == mintemp == maxtemp:
        pass
    else:
        temp = '{} (Max: {}°C, Min: {}°C)'.format(temp, maxtemp, mintemp)
    status = results['weather'][0]['description']
    if lang == 'en':
        status = ["City: {}".format(city),
                  "Temperature: {}°C".format(temp),
                  "Humidity: {}%".format(humidity),
                  "Clouds: {}%".format(clouds),
                  "Wind: {} km/h - {}".format(wind, status)]

    if lang == 'it':
        status = ['Città: {}'.format(city),
                  'Temperatura: {}'.format(temp),
                  'Umidità: {}'.format(humidity),
                  'Nuvolosità: {}'.format(clouds),
                  'Vento: {} km/h - {}'.format(wind, status)]

    return ' · '.join(status)

def cmd_ym(args, lang='en'):
    city = ' '.join(args['<city>'])
    api = 'http://weather.yahooapis.com/forecastrss'
    options = '?u=c&q={}'.format(city.replace(' ', '_'))
    url = '{}{}'.format(api, options)
    page = urllib.request.urlopen(url)
    results = feedparser.parse(page)
    if results.entries[0]['title'] == 'City not found':
        if lang == 'en':
            return 'No results for "{}"'.format(city)
        if lang == 'it':
            return 'Nessun risultato per "{}"'.format(city)
    feed = results['feed']
    city = '{}, {}'.format(feed.yweather_location['city'],
                           feed.yweather_location['country'])
    speed = float(feed.yweather_wind['speed'])
    wind = '{} {}'.format(speed, feed.yweather_units['speed'])
    humidity = '{}%'.format(feed.yweather_atmosphere['humidity'])
    if feed.yweather_atmosphere['visibility']:
        visibility = '{} {}'.format(feed.yweather_atmosphere['visibility'],
                                    feed.yweather_units['distance'])
    else:
        if lang == 'en':
            visibility = 'Not avaible at the moment'
        if lang == 'it':
            visibility = 'Non disponibile al momento'
    temp = results.entries[0].yweather_condition['temp']
#   Beaufort scale
    if lang == 'en':
        if speed < 1:
            description = 'Calm'
        elif speed < 4:
            description = 'Light air'
        elif speed < 8:
            description = 'Light breeze'
        elif speed < 12:
            description = 'Gentle breeze'
        elif speed < 19:
            description = 'Moderate breeze'
        elif speed < 25:
            description = 'Fresh breeze'
        elif speed < 32:
            description = 'Strong breeze'
        elif speed < 39:
            description = 'Near gale'
        elif speed < 47:
            description = 'Gale'
        elif speed < 55:
            description = 'Strong gale'
        elif speed < 64:
            description = 'Storm'
        elif speed < 73:
            description = 'Violent storm'
        else:
            description = 'Hurricane'
        status = ['City: {}'.format(city),
                  'Temperature: {}°C'.format(temp),
                  'Humidity: {}'.format(humidity),
                  'Visibility: {}'.format(visibility),
                  'Wind: {} - {}'.format(wind, description)]
    if lang == 'it':
        if speed < 1:
            description = 'Calmo'
        elif speed < 4:
            description = 'Vento leggero'
        elif speed < 8:
            description = 'Brezza leggera'
        elif speed < 12:
            description = 'Brezza gentile'
        elif speed < 19:
            description = 'Brezza moderata'
        elif speed < 25:
            description = 'Brezza fresca'
        elif speed < 32:
            description = 'Strong breeze'
        elif speed < 39:
            description = 'Nei presso di una burrasca'
        elif speed < 47:
            description = 'Burrasca'
        elif speed < 55:
            description = 'Forte burrasca'
        elif speed < 64:
            description = 'Tempesta'
        elif speed < 73:
            description = 'Forte tempesta'
        else:
            description = 'Uragano'
    status = ['Città: {}'.format(city),
              'Temperatura: {}°C'.format(temp),
              'Umidità: {}'.format(humidity),
              'Visibilità: {}'.format(visibility),
              'Vento: {} - {}'.format(wind, description)]
    return ' · '.join(status)
