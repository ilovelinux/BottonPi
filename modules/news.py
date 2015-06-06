# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import urllib.request
import json
import random

@command
def googlenews(self, mask, target, args):
    """Google News

        %%googlenews <news>...
    """
    return cmd_googlenews(self, mask, target, args)
    
@command
def gn(self, mask, target, args):
    """Google News

        %%gn <news>...
    """
    return cmd_googlenews(self, mask, target, args)
    
def cmd_googlenews(self, mask, target, args):
    argomento = ' '.join(args['<news>']).replace(' ', '%20')
    url = 'https://ajax.googleapis.com/ajax/services/search/news?v=1.0&h1=IT&ned=it&q='
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/31.0.1636.0 Safari/537.36'
    }
    try:
        requrl = urllib.request.Request('{}{}'.format(url, argomento), None, header)
        finurl = urllib.request.urlopen(requrl).read()
    except:
        return 'Impossibile connettersi al momento'
    results = json.loads(finurl.decode('utf8'))
    base = results['responseData']['results']
    if not base:
        return 'Nessun risultato per {}'.format(' '.join(args['<news>']))
    rand = random.choice(base)
    try:
        newsurl = rand['image']['originalContextUrl']
    except:
        newsurl = urllib.parse.unquote(rand['url'])
#     argomento = results['responseData']['results'][rand]['content']
    titolo = rand['titleNoFormatting']
    if '<b>' in titolo:
        titolo = titolo.replace('<b>', '')
    if '</b>' in titolo:
        titolo = titolo.replace('</b>', '')
    if '&#39;' in titolo:
        titolo = titolo.replace('&#39;', '’')
    lingua = rand['language'].upper()
    autore = rand['publisher']
    return '{} - {}: {} | Lingua: {}'.format(autore, titolo, newsurl, lingua)
