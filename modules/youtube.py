from irc3.plugins.command import command
import bs4
import urllib.request

@command
def youtube(self, mask, target, args):
        """Youtube video search

           %%youtube <search>...
        """
        return youtube_cmd(self, mask, target, args)

@command
def y(self, mask, target, args):
    """Youtube video search
      
      %%youtube <search>...
    """
    return youtube_cmd(self, mask, target, args)

def youtube_cmd(self, mask, target, args):
    inpt = args['<search>']
    query = '%20'.join(inpt)
    text = ' '.join(inpt)
    url = 'http://youtu.be/'
    search = 'https://www.youtube.com/results?search_query={}'.format(query)
    page = bs4.BeautifulSoup(urllib.request.urlopen(search))
    if page.find('div', {'class':'search-message'}):
        title = page.find('div', {'class':'search-message'}).text
        return 'Youtube <{}>: {}'.format(text, title)
    else:
        result = page.find('ol', {'class':'item-section'})
        result = result.find('li')
        result = result.find('div')
        result = result.find('div', {'class':'yt-lockup-dismissable'})
        result = result.find('div', {'class':'yt-lockup-content'})
        result = result.find('h3', {'class':'yt-lockup-title'})
        result = result.a
        title = result.text
        url = '{}{}'.format(url, result['href'].strip('/watch?v='))
        return 'Youtube <{}>: {} url: {}'.format(text, title, url)
