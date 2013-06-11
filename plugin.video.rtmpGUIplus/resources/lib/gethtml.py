# -*- coding: UTF-8 -*-
'''
gethtml with cookies support  v1
by anarchintosh @ xbmcforums
Copyleft = GNU GPL v3 (2011 onwards)

this function is paired with weblogin.py
and is intended to make it easier for coders wishing
to scrape source of pages, while logged in to that site.
'''

import urllib,urllib2
import cookielib
import os
import re
cookiepath = "special://temp/"

#Listas de URLS Compatibles
compatible_urllist = ['http://xbmcspain.com/']


def url_for_cookies(url):
    for compatible_url in compatible_urllist:
        
        if re.search(compatible_url,url):    
            url_is_compatible = True
            break

        else: url_is_compatible = False
        
    return url_is_compatible        

def get(url,cookiepath=None):
    if cookiepath is not None:

        if url_for_cookies(url) == True:

                if not os.path.isfile(cookiepath):
                    cookiepath = os.path.join(cookiepath,'cookies.lwp')

                if os.path.exists(cookiepath):
                 
                    cj = cookielib.LWPCookieJar()
                    cj.load(cookiepath)
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')   
                    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                    response = opener.open(req)
                    link=response.read()
                    response.close()
                    return link
               
                else: return _loadwithoutcookies(url)                
        else: return _loadwithoutcookies(url)    
    else: return _loadwithoutcookies(url)

def _loadwithoutcookies(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')   
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link  
