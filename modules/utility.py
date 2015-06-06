from irc3.plugins.command import command
import random
import datetime
import time
import bs4
import urllib
import builtins

@command
def rand(self=None, mask=None, target=None, args=None):
    """Sceglie una parola a caso

        %%rand <parole>...
    """
    parole = args['<parole>']
    if builtins.len(parole) == 1:
        return 'Inserire due o più parole'
    rand = random.choice(parole)
    return 'Random <{}>: {}'.format(', '.join(parole), rand)

@command
def leet(self=None, mask=None, target=None, args=None):
    """Trasforma le lettere in numeri

        %%leet <parole>...
    """
    leet = ''
    parole = ' '.join(args['<parole>'])
    for lettere in parole:
        if 'a' in lettere or 'A' in lettere:
            leet += '4'
        elif 'o' in lettere or 'O' in lettere:
            leet += '0'
        elif 'i' in lettere or 'I' in lettere:
            leet += '1'
        elif 'e' in lettere or 'E' in lettere:
            leet += '3'
        elif 's' in lettere or 'S' in lettere:
            leet += '5'
        elif 't' in lettere or 'T' in lettere:
            leet += '7'
        else:
            leet += lettere.upper()
    return 'Leet <{}>: {}'.format(parole, leet)

@command
def source(self=None, mask=None, target=None, args=None):
    """Indica i codici sorgente

        %%source
    """
    return 'https://bitbucket.org/ilovelinux/bottonpi/src'

@command
def countdown(self=None, mask=None, target=None, args=None):
    """Conto alla rovescia

        %%countdown <secs>
    """
    countdown = ''.join(args['<secs>'])
    try:
        int(countdown)
    except:
        return 'Inserire una misura valida in secondi'
    time.sleep(int(countdown))
    return 'Conto alla rovescia terminato'

@command
def uptime(self=None, mask=None, target=None, args=None):
    """Indica l'uptime del dispositivo in cui è hostato

        %%uptime
    """
    with open('/proc/uptime', 'r') as up:
        time = float(str(up.readline().split()[0]))
    base = str(datetime.timedelta(seconds = time)).replace('days', 'giorni').split('.')
    return 'Uptime: {} e {} secondi.'.format(base[0], base[1][:2])

@command
def test(self=None, mask=None, target=None, args=None):
    """Frase al contrario

        %%test <t>...
    """
    return 'self: {}; mask: {}; target:{}; args:{} ({});'.format(self, mask, target, args,  ' '.join(args['<t>']))

@command
def reverse(self=None, mask=None, target=None, args=None):
    """Frase al contrario

        %%reverse <rev>...
    """
    rev = ' '.join(args['<rev>'])
    return 'Reverse <{}>: {}'.format(rev, rev[::-1])

@command
def len(self=None, mask=None, target=None, args=None):
    """misura la lunghezza delle stringhe

        %%len <text>...
    """
    text = ' '.join(args['<text>'])
    return 'Lenght <{}>: {}'.format(text, str(builtins.len(text)))

@command
def forum(self=None, mask=None, target=None, args=None):
    """Info sulle statistiche del forum

        %%forum <forum>...
    """
    forum = ' '.join(args['<forum>'])
    forums = {
            'Ubuntu It': 'http://forum.ubuntu-it.org/index.php',
            'SpeedCubing.it': 'http://speedcubing.it/forum/stats.php',
            'TNTVillage':'http://forum.tntvillage.scambioetico.org/index.php',
    }
    if 'ubuntu' in forum.lower(): 
        page = bs4.BeautifulSoup(urllib.request.urlopen(forums['Ubuntu It']))
        stats = page.find_all('strong')
        totalmsg = 'Totale messaggi: {}'.format(stats[16].text)
        totalthreads = 'Totale discussioni: {}'.format(stats[17].text)
        totaluser = 'Totale iscritti: {}'.format(stats[18].text)
        lastuser = 'Ultimo iscritto: {}'.format(stats[19].a.text)
        return '{} · {} · {} ({})'.format(totalmsg, totalthreads, totaluser, lastuser)
    if 'speedcubing' in forum.lower():
        page =  bs4.BeautifulSoup(urllib.request.urlopen(forums['SpeedCubing.it']))
        stats = page.find('table', {'border':"0", 'cellpadding':"4", 'cellspacing':"1", 'class':"tborder"})
        total = ' · '.join(stats.find('td', {'class':"trow1", 'valign':"top"}).text.split('\r\n'))
        medie = ' · '.join(stats.find('td', {'class':"trow1", 'rowspan':'3', 'valign':"top"}).text.split('\r\n'))
        general = ' · '.join(stats.find_all('td', {'class':"trow1"})[2].text.split('\r\n'))
        return ['Totale: {}'.format(total), 'Medie: {}'.format(medie), 'Generale: {}'.format(general)]
#        stats = page.find_all('span', {'class':'smalltext'})[65].text
#        stats = stats[1:].replace(',', '.').replace('o.', 'o:')
#        stats = stats.replace('.\n', ' · ')[:-1].replace('Il', '· Il')
        return stats
    if 'tntvillage' in forum.lower():
        page = bs4.BeautifulSoup(urllib.request.urlopen(forums['TNTVillage']))
        stats = page.find_all('td', {'align':'left', 'class':'row4', 'width':'95%'})
        torrents = stats[1].text.replace(')', ') · ')
        users = stats[0].text.replace('A', ' · A').replace('L', ' · L')
        users = users.replace('I', ' · I')
        return ['Forum: {}'.format(users), 'Torrents: {}'.format(torrents)]

    return 'Forum non ancora supportato'

@command
def title(self=None, mask=None, target=None, args=None):
    """Return the page title
        %%title <url>
    """
    url = [args['<url>']] * 2
    for part in url[0].split('/'):
        if 'www' in part and '.' in part:
            url[1] = part
    try:
        title = bs4.BeautifulSoup(urllib.request.urlopen(url[0])).title.text
        return 'Il titolo di "{}" è "{}"'.format(url[1], title)
    except:
        return 'Impossibile aprire il seguente link: {}'.format(url[0])
