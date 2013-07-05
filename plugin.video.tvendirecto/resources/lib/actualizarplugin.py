import urllib, os,re,urllib2
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, main
opciones = xbmcaddon.Addon()
 
def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("Actualizaciones","Descargando archivo")
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED"
        dp.close()
 
url ='http://playstationstorelibre.eshost.es/descargas/plugin.video.tvendirecto.zip'
DownloaderClass(url, opciones.getAddonInfo('path')+"/actualizaciones/plugin.video.tvendirecto.zip")
