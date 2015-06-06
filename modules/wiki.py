from irc3.plugins.command import command
import urllib.request
import json

@command
def wikipedia(self, mask, target, args):
    """Indica il meteo della città

        %%wikipedia <search>...
    """
    return cmd_wikipedia(args)
    
@command
def wiki(self, mask, target, args):
    """Indica il meteo della città

        %%wiki <search>...
    """
    return cmd_wikipedia(args)

def cmd_wikipedia(args):
    ricerca = ' '.join(args['<search>'])
    ricerca1 = ricerca.replace(' ', '%20')
    searchurl = 'http://it.wikipedia.org/w/api.php?format=json&action=query&list=search&srlimit=1&srprop=timestamp&srwhat=text&srsearch='
    try:
        searchopen = urllib.request.urlopen(searchurl + ricerca1).read()
    except:
        return 'Impossibile connettersi al momento'
    searchresults = json.loads(searchopen.decode('utf8'))
    if not searchresults['query']['search']:
        return 'Nessun risultato per {}'.format(ricerca, args)
    title = searchresults['query']['search'][0]['title']
    title1 = title.replace(' ', '%20')
    url = 'https://it.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&exchars=300&redirects&titles='
    open = urllib.request.urlopen(url + title1).read()
    results = json.loads(open.decode('utf8'))
#    if results['query']['pages']['-1']:
#        return 'Nessun risultato per {}'.format(ricerca)
    link = 'https://it.wikipedia.org/wiki/{}'.format(title1)
    info = results['query']['pages']
    info = info[list(info.keys())[0]]['extract']
    return '{}: {} Fonte: {}'.format(title, info, link)
