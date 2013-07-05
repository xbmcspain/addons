#!/usr/bin/env python
# -*- coding: utf-8 -*-
# main.py - rtmpGUI extension withEPG
# (C) 2012 HansMayer,BlueCop - http://supertv.3owl.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib, urllib2, cookielib
import string, os, re, time, sys, weblogin, gethtml
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
__settings__   = xbmcaddon.Addon()

from aes import AESCtr
from epg import *

#Carpeta de las imagenes
carpetaimagenes = os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'resources/imagenes/')

#Actualizaciones
Actualizacionn = os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'actualizaciones/plugin.video.tvendirecto.zip')
RUTAPLUGIN = os.path.join(xbmcaddon.Addon().getAddonInfo('path'))

#Iconos de las notificaciones
notierror = os.path.join(__settings__.getAddonInfo('path'),'resources/imagenes/noti_error.png')
notiinf = os.path.join(__settings__.getAddonInfo('path'),'resources/imagenes/noti_informa.png')
notimail = os.path.join(__settings__.getAddonInfo('path'),'resources/imagenes/noti_mail.png')

ArchivoFavoritos = os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'resources/Favoritos.xml')
LogoDefecto = os.path.join(__settings__.getAddonInfo('path'),'icon.png')
LogoD = os.path.join(__settings__.getAddonInfo('path'),'resources/imagenes/adultos.png')
Ventana = xbmcgui.Window()


#Menu Contextual en desarrollo
MENUDIALOGO = xbmcgui.Dialog()
MENUCONTEXTUAL = xbmcgui.ListItem()
ACTION_CONTEXT_MENU = 100

dialogo = xbmcgui.Dialog()
cookiepath = __settings__.getAddonInfo('Path')
use_account = __settings__.getSetting('use-account')
username = __settings__.getSetting('username')
password = __settings__.getSetting('password')
version = xbmcaddon.Addon().getAddonInfo('version')
url = "http://xbmcspain.com/foro/ucp.php?mode=login&redirect=.%2Findex.php"
source = gethtml.get(url)

try:
    try:
        raise
        import xml.etree.cElementTree as ElementTree
    except:
        from xml.etree import ElementTree
except:
    try:
        from elementtree import ElementTree
    except:
        dlg = xbmcgui.Dialog()
        dlg.ok('ElementTree missing', 'Please install the elementree addon.',
                'http://tinyurl.com/xmbc-elementtree')
        sys.exit(0)
        
def MensajeBienvenida():
	msgBienve = __settings__.getSetting('msgBienvenida')
	
	if msgBienve is not True:
		Bienve = dialogo.ok('Bienvenido/a', 'Esta es la primera gran actualizacion que le hago al plugin')
		msgBienve = __settings__.setSetting('msgBienve','true')

def Notificaciones(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def LOGIN(username,password,hidesuccess):
	uc = username[0].upper() + username[1:]
	lc = username.lower()
	hidesuccess = __settings__.getSetting('hide-successful-login-messages')
	logged_in = weblogin.doLogin(cookiepath,username,password)
	
	# Comprueba si esta logeado, y si lo esta, ejecuta las acciones
	if logged_in == True:
		# Debajo de esta linea iran las opciones especiales de los que esten logeados
		#############################################################################
		#############################################################################
		
		#si Desactivar Notificaciones esta Desactivado, envia todas las notificaciones que haya, tanto avisos, errores etc
		if hidesuccess == 'false':
			pass

	# Si no esta logeado te manda el error de login, y las funciones que se añadan para los desconectados.
	if logged_in == False:
		Notificaciones('Error de Login',username+' Comprueba tus datos.','4000',notierror)

def STARTUP_ROUTINES():
        #deal with bug that happens if the datapath doesn't exist
        if not os.path.exists(cookiepath):
          os.makedirs(cookiepath)

        use_account = __settings__.getSetting('use-account')

        if use_account == 'true':
             #get username and password and do login with them
             #also get whether to hid successful login notification
             username = __settings__.getSetting('username')
             password = __settings__.getSetting('password')
             hidesuccess = __settings__.getSetting('hide-successful-login-messages')

             LOGIN(username,password,hidesuccess)

def addFolder(BASE, source=None, lang='', iconImage='', totalItems=0):
    if not lang:
        #title=urllib.unquote(BASE[source].split('/')[-1][:-4])
        title = BASE[source][1]
    else:
        title=lang
    
	'''
    elif title == 'Respaldo TV Espña':
        item=xbmcgui.ListItem(title, iconImage=carpetaimagenes+'backuptv.png')
        item.setInfo( type="Video", infoLabels={ "Title": title })
		
    elif title == 'Series Espña':
        item=xbmcgui.ListItem(title, iconImage=carpetaimagenes+'esp.png')
        item.setInfo( type="Video", infoLabels={ "Title": title })
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0]+"?src="+str(source)+"&lang="+lang,listitem=item,isFolder=True,totalItems=totalItems)
	
    elif title == 'Canales Adltos':
        item=xbmcgui.ListItem(title, iconImage=carpetaimagenes+'adultos.png')
        item.setInfo( type="Video", infoLabels={ "Title": title })
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0]+"?src="+str(source)+"&lang="+lang,listitem=item,isFolder=True,totalItems=totalItems)
		
    elif title == 'TV Ruana':
        item=xbmcgui.ListItem(title, iconImage=carpetaimagenes+'esp.png')
        item.setInfo( type="Video", infoLabels={ "Title": title })
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0]+"?src="+str(source)+"&lang="+lang,listitem=item,isFolder=True,totalItems=totalItems)
    else:
        pass
        #item=xbmcgui.ListItem(title, iconImage=os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'icon.png'))
        #item.setInfo( type="Video", infoLabels={ "Title": title })
        #xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0]+"?src="+str(source)+"&lang="+lang,listitem=item,isFolder=True,totalItems=totalItems)
	'''	
		
    #-------------------------------
	# Esto es el Default del plugin.
    item=xbmcgui.ListItem(title, iconImage=LogoDefecto)
    item.setInfo( type="Video", infoLabels={ "Title": title })
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0]+"?src="+str(source)+"&lang="+lang,listitem=item,isFolder=True,totalItems=totalItems)
    
def addFolderC(BASE, source=None, title='', i=0, totalItems=0, thumb=''):
    item=xbmcgui.ListItem(title, iconImage=thumb)
    item.setInfo( type="Video", infoLabels={ "Title": title })
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0]+"?src="+str(source)+"&channel="+str(i),listitem=item,isFolder=True,totalItems=totalItems)

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[-1]=='/'):
            params=params[0:-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in pairsofparams:
            splitparams={}
            splitparams=i.split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

def checkAutoupdateEPG():
    if os.popen('uname').read().strip() == 'Darwin':
        if not os.path.exists(os.path.expanduser('~/Library/LaunchAgents/com.xbmc.tvendirecto.plist')):
            launch = True
        else:
            launch = False
        cmd='cp "'+os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'resources/com.xbmc.tvendirecto.plist')
        os.system(cmd+'" "'+os.path.expanduser('~/Library/LaunchAgents/')+'"')
        if launch:
            os.system('launchctl load "'+os.path.expanduser('~/Library/LaunchAgents/com.xbmc.tvendirecto.plist')+'"')
            
def playItem(params):
    listitem = xbmcgui.ListItem(label=urllib.unquote(params['title']), iconImage=urllib.unquote(params['logo']), path=params['link'])
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
    xbmc.executebuiltin("Container.SetViewMode(503)")
    
def filmOnUpdate(params):
    link=urllib.unquote(params['link'])
    chanid=link.split(' ')[0].split('?')[0].split('live')[1]
    quality=link.split(' ')[1].split('=')[1].split('.')[1]
    phpsessid=downloadSocket('www.filmon.com',80).fetch('GET /ajax/getChannelInfo HTTP/1.1\r\nHost: www.filmon.com\r\nConnection:close\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19\r\n\r\n').split('PHPSESSID=')[1].split(";")[0]
    headers=[('Origin','http://www.filmon.com'),('Referer','http://www.filmon.com/tv/htmlmain/'),('X-Requested-With','XMLHttpRequest'),('Accept','application/json, text/javascript, */*'),('Connection','keep-alive'),('Cookie','disable-edgecast=1; viewed_site_version_cookie=html;PHPSESSID='+phpsessid+";")]
    a=getURL('http://www.filmon.com/ajax/getChannelInfo', post=urllib.urlencode({'channel_id':chanid, 'quality':quality}),headers=headers,ct=True)

    params['link'] = json.loads(a)[0]['serverURL']+' playpath='+json.loads(a)[0]['streamName']+" app=live/"+json.loads(a)[0]['serverURL'].split('/')[-1]+" "+" ".join(link.split(' ')[2:])
    playItem(params)

'''    
def update45ESToken(params):
    link=urllib.unquote(params['link'])
    playpath=re.findall('playpath=(?P<playpath>.*?) ',link)[0]
    rtmplink = link.split(' ')[0]
    directo=AESCtr().encrypt(getURL('http://servicios.telecinco.es/tokenizer/clock.php')+";"+playpath+";0;0", "xo85kT+QHz3fRMcHMXp9cA", 256)
    data=getURL('http://servicios.telecinco.es/tokenizer/tk3.php',post=urllib.urlencode({'id':playpath,'startTime':'0','directo':directo,'endTime':'endTime'}))
    #params['link'] = link.replace('playpath='+playpath, 'playpath='+ElementTree.XML(data).findtext('file'))
    xdata = ElementTree.XML(data)
    params['link'] = link.replace('playpath='+playpath, 'playpath='+xdata.findtext('file')).replace(rtmplink, xdata.findtext('stream'))
    playItem(params)
'''
    
def listSources(BASE):
    if len(BASE) < 2:
        listLanguages(BASE)
        return
		
    for source in BASE:
        addFolder(BASE,BASE.index(source),totalItems=len(BASE))
    #xbmc.executebuiltin("Container.SetViewMode(502)")
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )
    
def listLanguages(BASE,src=0):
    xml=getURL(BASE[int(src)][0],None)
    #tree = ElementTree.XML(xml)
    tree = ElementTree.parse(StringIO(xml)).getroot()
    if len(tree.findall('channel')) > 0:
        listChannels(BASE,src)
        return
    streams = tree.findall('stream')
    languages = []
    for stream in streams:
        language = stream.findtext('language').strip()
        if not language in languages and language.find('Link Down') == -1:
            languages.append(language)
            
    languages = list(set(languages))
    languages.sort()

    if len(languages) < 2:
        listVideos(BASE,src, languages[0])
        return

    for lang in languages:
        addFolder(BASE,src, lang, totalItems=len(languages))
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )

def listVideos(BASE,src=0,lang='',chan=-1):
    xml=getURL(BASE[int(src)][0],None)
    #tree = ElementTree.XML(xml)
    tree = ElementTree.parse(StringIO(xml)).getroot()
    hasEPG=False
    newS=[]
    if chan > -1:
        newS = tree.findall('channel')
        print newS
        newS = newS[chan].findall('items')[0].findall('item')
    else:
        streams = tree.findall('stream')
        for stream in streams:
            language = stream.findtext('language').strip()
            if language == lang and language.find('Link Down') == -1 :
                newS.append(stream)
    
    for stream in newS:
        title = '[B]'+stream.findtext('title')+'[/B]'
        desc = title
        epgid=stream.findtext('epgid', None)
        EPGactivo = __settings__.getSetting('activarEPG')
        if EPGactivo == 'false':
            pass
        else:
            if epgid:
                ep=epgid.split(":")
                if ep[0] in EPGs.keys():
				    e=EPGs[ep[0]](ep[1])
				    hasEPG = True
				    desc = ""
				    epg=e.getEntries()
				    i=len(epg)
				    for e in epg:
				        if (__settings__.getSetting("show24h") == 'false'):
				            desc += e[1].strftime("%I:%M")+'-'+e[2].strftime("%I:%M")+":\n"+e[0]+u"\n\n"
				        else:
				            desc += e[1].strftime("%H:%M")+'-'+e[2].strftime("%H:%M")+":\n"+e[0]+u"\n\n"
				    if len(epg) > 0:
				        title +=' - '+epg[0][0]
        rtmplink = stream.findtext('link',' ').strip()
        if rtmplink[:4] == 'rtmp':
            if stream.findtext('playpath'):
                rtmplink += ' playpath='+stream.findtext('playpath').strip()
            if stream.findtext('swfUrl'):
                rtmplink += ' swfurl='+stream.findtext('swfUrl').strip()
            if stream.findtext('pageUrl'):
                rtmplink += ' pageurl='+stream.findtext('pageUrl').strip()
            if stream.findtext('proxy'):
                rtmplink += ' socks='+stream.findtext('proxy').strip()
            if stream.findtext('advanced','').find('live=') == -1 and rtmplink.find('mms://') == -1 and rtmplink.find('http://') != 0:
                rtmplink += ' live=1 '
            if rtmplink[:4] == 'rtmp':
                rtmplink += ' timeout=30 '+stream.findtext('advanced','').replace('-v','').replace('live=1','').replace('live=true','')
            if (__settings__.getSetting("has_updated_librtmp") == 'true'):
                rtmplink = rtmplink.replace('-x ',"swfsize=").replace('-w ','swfhash=')    
        logo=stream.findtext('logourl', "DefaultTVShows.png")
        if chan > -1:
            logo=stream.findtext('thumbnail', "DefaultTVShows.png")
        item=xbmcgui.ListItem(title, iconImage=logo)
        infolabels = { "title": title, "plot": desc, "plotoutline": desc, "tvshowtitle": title, "originaltitle": title}
        item.setInfo( type="video", infoLabels=infolabels )
        item.setProperty('IsPlayable', 'true')
        #-------Estas lineas en coment funcionan NO TOCAR------#
        #argsAdd = str('OpcionesAddon()')
        #runnerAdd = "XBMC.RunAddon(plugin.video.tvendirecto)"
        #commands = []
        #commands.append(( ' _______[Favoritos]_______', 'XBMC.RunPlugin(plugin://video/myplugin)', ))
        #commands.append(( '|  Añadir a Favoritos              |', 'XBMC.RunPlugin(plugin://video/myplugin)', ))
        #commands.append(( 'Eliminar de Favoritos', runnerAdd, ))
        #commands.append(( 'Añadir a Favoritos', 'XBMC.RunPlugin(plugin://video/myplugin)', ))
        #commands.append(( 'runother', 'XBMC.RunPlugin(plugin://video/otherplugin)', ))
        #item.addContextMenuItems( commands, replaceItems = True )
        #-------------------------------------------------------#
        xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content='movies' )
        if stream.findtext('swfUrl') == 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=f':
            rtmplink = sys.argv[0]+"?tk=filmon&link="+urllib.quote(rtmplink)+"&title="+urllib.quote(title.encode('utf-8'))+"&logo="+urllib.quote(logo)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=rtmplink.strip(),listitem=item,isFolder=False,totalItems=len(newS))

    if hasEPG:
        xbmc.executebuiltin("Container.SetViewMode(503)")
    else:
        xbmc.executebuiltin("Container.SetViewMode(502)")
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )
    #MenuEmer = ['Añadir a Favoritos','Eliminar de Favoritos']
    #ret = MENUDIALOGO.select('Choose a playlist', MenuEmer)
	
def comprobarActualizaciones():
	ErrorArchivo = 'ERROR'
	XML = urllib.urlopen('http://playstationstorelibre.eshost.es/descargas/addon.xml')
	Leer = XML.read()
	XML.close()
	print Leer # en el log del xbmc escribe la version del xml

	if re.search(ErrorArchivo,Leer,re.IGNORECASE):
		print 'comprobarActualizaciones: Error... El archivo que comprueba las versiones del plugin no existe.'
		print 'comprobarActualizaciones: Error... El archivo que comprueba las versiones del plugin no existe.'
		print 'comprobarActualizaciones: Error... El archivo que comprueba las versiones del plugin no existe.'
		return True
	else:
		if os.path.isfile(Actualizacionn) == True:
			ContinuarActualizacion = dialogo.yesno('Instalar Actualización','Has descargado una actualizacion pero','no la as instalado... Instalarla?')
			if ContinuarActualizacion == True:
				zip = zipfile.ZipFile(Actualizacionn)
				zip.extractall(RUTAPLUGIN)
				zip.close()
				os.remove(Actualizacionn)
				xbmc.executebuiltin("UpdateLocalAddons")
				dialogo.ok('Instalación Completa','Se ha instalado la actualización correctamente','Inicia el plugin de nuevo!')
				xbmc.executebuiltin("XBMC.Container.Update(addons://sources/video/, replace)")
			else:
				InstAct = dialogo.ok('Instalar Actualización','Cuando inicies otra vez el plugin','Se te volvera a preguntar')
				#xbmc.executebuiltin("XBMC.Container.Update(addons://sources/video/, replace)")
		else:
			if version < Leer:
				Actualizacion = dialogo.yesno('Nueva Actualización', '¿Quieres descargarla ahora?')
				if Actualizacion == True:
					from resources.lib.actualizarplugin import DownloaderClass
					quieresactualizar = dialogo.yesno('Instalar Actualización', '¿Quieres instalar la actualización ahora?')
					if quieresactualizar == True:
						zip = zipfile.ZipFile(Actualizacionn)
						zip.extractall(RUTAPLUGIN)
						zip.close()
						os.remove(Actualizacionn)
						xbmc.executebuiltin("UpdateLocalAddons")
						dialogo.ok('Instalación Completa','Se ha instalado la actualización correctamente','Inicia el plugin de nuevo!')
						xbmc.executebuiltin("XBMC.Container.Update(addons://sources/video/, replace)")
					else:
						luego = dialogo.ok('Instalar Despues', 'Cuando inicies otra vez el plugin','Se te volvera a preguntar')
				else:
					adios = dialogo.ok('Actualización Recomendada', 'Es necesario que instales la actualización','La proxima vez instalala, para mejorar el plugin')
			else:
				pass
				

def main(BASE):
    '''dialogo.notification('Notificación','Prueba del mensaje de notificaciones de xbmcgui.dialog() de la version GOTHAM',xbmcgui.NOTIFICATION_INFO,5000)'''
    parms=get_params()
    if 'link' in parms and 'tk' in parms:
        '''if parms['tk'] == 'telecinco':
            update45ESToken(parms)'''
        if parms['tk'] == 'filmon':
            filmOnUpdate(parms)
    if "src" in parms and 'lang' in parms and parms['lang']:
        listVideos(BASE,parms['src'], parms['lang'])
    elif "src" in parms and 'channel' in parms and parms['channel']:
        listVideos(BASE,parms['src'], chan=int(parms['channel']))
    elif 'src' in parms:
        listLanguages(BASE,parms['src'])
    else:
        checkAutoupdateEPG()
        listSources(BASE)
        comprobarActualizaciones()
        
	msgBienve1 = __settings__.getSetting('msgBienvenida')
	
	if msgBienve1 == 'false':
		msgBienve1 = __settings__.setSetting('msgBienvenida','true')
		Bienve = dialogo.ok('Bienvenido/a', 'Esta es la primera versión pública','del plugin, así que...','¡espero que os guste! :)')
		
	STARTUP_ROUTINES()
