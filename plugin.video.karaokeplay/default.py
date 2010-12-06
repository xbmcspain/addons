import urllib2,re,xbmcplugin,xbmcgui,os
from urlparse import urlsplit
from urllib import quote_plus, unquote_plus, urlencode
from BeautifulSoup import BeautifulSoup
from cgi import parse_qs

base_url = 'http://www.karaokeplay.com'
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


def main_menu():
    addDir('Search by title','/', act='search', search_by='Title')
    addDir('Search by artist','/', act='search', search_by='Artist')
    addDir('Latest','/songs/new_songs', act='show_page')
    addDir('Browse by Title','/songs/browse', act='browse')
    addDir('Browse by Artist','/artists/browse/', act='browse')
    addDir('Genre: 80\'s','/genres/80s.html', act='show_genre')
    addDir('Genre: Children','/genres/Children.html', act='show_genre')
    addDir('Genre: Christian','/genres/Christian.html', act='show_genre')
    addDir('Genre: Classics','/genres/Classics.html', act='show_genre')
    addDir('Genre: Country','/genres/Country.html', act='show_genre')
    addDir('Genre: Duets','/genres/Duets.html', act='show_genre')
    addDir('Genre: Hip-Hop','/genres/Hip-Hop.html', act='show_genre')
    addDir('Genre: Holiday','/genres/Holiday.html', act='show_genre')
    addDir('Genre: Love Songs','/genres/Love Songs.html', act='show_genre')
    addDir('Genre: Oldies','/genres/Oldies.html', act='show_genre')
    addDir('Genre: Pop','/genres/Pop.html', act='show_genre')
    addDir('Genre: RnB','/genres/RnB.html', act='show_genre')
    addDir('Genre: Rock','/genres/Rock.html', act='show_genre')

def show_page(url):
    print 'Show page: %s' % unquote_plus(url).replace('&amp;','&')
    link = fetch_page(unquote_plus(url))
    soup = BeautifulSoup(link)
    next_page = soup.find('a', {'class': 'next_page'})
    if next_page:
        addDir('Next page', next_page['href'], act='show_page')

    for tag in soup.findAll('div', {'class': 'songInfo'}):
        links = tag.findAll('a')
        if len(links) == 1:
            artist = links[0]
            addDir(artist.text,
                   artist['href'],
                   act='show_page')
        else:
            song,artist = tag.findAll('a')
            addDir("%s by %s" % (song.text, artist.text),
                    song['href'],
                    is_folder=False,
                    act='play')

def show_genre(url):
    addDir('Filter by letter',
           urlsplit(url)[2].replace('genres','genres/browse'),
           act='browse',
           append='?letter=')
    show_page(url)

def search_videos(name, search_by):
    search_entered = ''
    keyboard = xbmc.Keyboard('', name)
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        search_entered = unicode( keyboard.getText(), "utf-8" )
    else:
        return False, 0
    title = quote_plus(search_entered)
    searchUrl = '%s/search?search[term]=%s&search[options]=%s' % (
                 base_url,
                 search_entered, 
                 search_by)

    link = fetch_page(searchUrl)
    soup = BeautifulSoup(link)
    next_page = soup.find('a', {'class': 'next_page'})
    if next_page:
         addDir('Next page', 
                '%s?%s' % (urlsplit(next_page['href'])[2:4]), #path
                act='show_page')

    for tag in soup.findAll('div', {'class': 'resultInfo left'}):
        links = tag.findAll('a')
        song,artist = tag.findAll('a')
        addDir("%s by %s" % (song.text, artist.text),
               song['href'],
               is_folder=False,
               act='play')

def play_video(url):
    link = fetch_page(url)
    match_obj = re.search(r'<link href=".*?&yt=(.+?)" rel="video_src" \/>', link)
    youtube_id = match_obj.group(1)
    xbmc_url = 'plugin://plugin.video.youtube/?path=/root/search/new&action=play_video&videoid=%s' % youtube_id
    xbmc.executebuiltin('XBMC.PlayMedia(%s)' % xbmc_url)


def fetch_page(url):
    req = urllib2.Request(url.replace(' ','%20')) #Doesn't seem to like spaces
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    html = response.read()
    response.close()
    return html 

def addDir(name, path, is_folder=True, **args):
    args['name'] = name.encode('utf-8')
    args['url'] = base_url + path
    full_url = "%s?%s" % (sys.argv[0], urlencode(args))
    listitem = xbmcgui.ListItem(name, iconImage="DefaultFolder.png")
    listitem.setInfo(type="Video", infoLabels={"Title": name})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                url=full_url,
                                listitem=listitem,
                                isFolder=is_folder)

def display_alphabet(url, append='/'):
    path = urlsplit(url)[2]
    addDir('All', path.replace('browse','').replace('//','/'), act='show_page')  
    for a in xrange(65,91):
        letter = chr(a)
        url = ''.join([path, append, letter])
        addDir(letter, url, act='show_page')

path = urlsplit(sys.argv[2])[2]
query = urlsplit(sys.argv[2])[3]
print "path: %s, query: %s" % (path, unquote_plus(query))
if query:
    params = parse_qs(query)
    for i in params.keys():
        params[i] = ''.join(params[i])
    print params
    action = params['act']
    if action == 'search':
        search_videos(params['name'],params['search_by'])
    elif action == 'play':
        play_video(params['url'])
    elif action == 'show_page':
        show_page(params['url'])
    elif action == 'browse':
        display_alphabet(params['url'],params.get('append','/'))
    elif action == 'show_genre':
        show_genre(params['url'])
else:
    main_menu()

xbmcplugin.endOfDirectory(int(sys.argv[1]))


