from irc3.plugins.command import command
import urllib.request
import json

@command
def twitch(self=None, mask=None, target=None, args=None):
    """Indica il meteo della città

        %%twitch <channel>...
    """
    channel = ' '.join(args['<channel>'])
    homeurl = 'http://www.twitch.tv/'
    streaming = '{}{}'.format(homeurl, channel.replace(' ', '%20'))
    url = 'https://api.twitch.tv/kraken/streams/{}'.format(channel.replace(' ', '%20'))
    try:
        opened = urllib.request.urlopen(url).read().decode('utf8')
    except urllib.error.HTTPError:
        return 'Il canale "{}" non è stato trovato'.format(channel)
    except:
        pass
    result = json.loads(opened)
    if not result['stream']:
        return '{} è offline'.format(channel)
    play = result['stream']['game']
    play = '{} è online e sta giocando a {}'.format(channel, play)
    viewers = result['stream']['viewers']
    views = result['stream']['channel']['views']
    statistiche = 'Visitatori: {} (Totali: {})'.format(viewers, views)
    followers = 'Followers: {}'.format(result['stream']['channel']['followers'])
    visitator = ' · '.join([statistiche, followers])
    return ['{} ({})'.format(play, visitator), 'Url: {}'.format(streaming)]
