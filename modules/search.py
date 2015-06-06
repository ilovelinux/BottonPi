# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import urllib.request
import json
import modules.wiki as wiki

@command
def google(self, mask, target, args):
    """Google Search

        %%google <search>...
    """
    return cmd_google(args)
    
@command
def g(self, mask, target, args):
    """Google Search

        %%g <search>...
    """
    return cmd_google(args)
    
@command
def googleit(self, mask, target, args):
    """Google Search
    
        %%googleit <search>...
    """
    return cmd_googleit(args)

def cmd_google(args):
    search = ' '.join(args['<search>']).replace(' ', '%20')
    url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&ie=UTF-8&q={}'.format(search)
    try:
        open = urllib.request.urlopen(url).read()
    except:
        return 'Impossibile collegarsi al momento'
    results = json.loads(open.decode('utf8'))
    base = results['responseData']['results']
    if not base:
        return 'Nessuno risultato per {}'.format(search.replace('%20', ' '))
    else:
        resurl = base[0]['unescapedUrl']
        if resurl[0:29] == 'http://it.wikipedia.org/wiki/' or resurl[0:30] == 'https://it.wikipedia.org/wiki/':
            return wiki.cmd_wikipedia(args)
        titolo = base[0]['titleNoFormatting']
#        contenuto = base[0]['content']
        return '{}: {}'.format(titolo, resurl)

def cmd_googleit(args):
        search = ' '.join(args['<search>']).replace(' ', '%20')
        url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&ie=UTF-8&lr=lang_it&q={}'.format(search)
        try:
            open = urllib.request.urlopen(url).read()
        except:
            return 'Impossibile collegarsi al momento'
        results = json.loads(open.decode('utf8'))
        base = results['responseData']['results']
        if not base:
            return 'Nessuno risultato per {}'.format(search.replace('%20', ' '))
        else:
            resurl = base[0]['unescapedUrl']
            if resurl[0:29] == 'http://it.wikipedia.org/wiki/' or resurl[0:30] == 'https://it.wikipedia.org/wiki/':
                return wiki.cmd_wikipedia(args)
            titolo = base[0]['titleNoFormatting']
#        contenuto = base[0]['content']
        return '{}: {}'.format(titolo, resurl)
