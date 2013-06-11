# -*- coding: UTF-8 -*-
"""
 weblogin
 by Anarchintosh @ xbmcforums
 Copyleft (GNU GPL v3) 2011 onwards
"""

import os
import re
import urllib,urllib2
import cookielib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

cookiepath = "special://temp/"
opciones = xbmcaddon.Addon()
NotiActiva = opciones.getSetting('hide-successful-login-messages')
#Iconos de las notificaciones
notierror = os.path.join(opciones.getAddonInfo('path'),'resources/imagenes/noti_error.png')
notiinf = os.path.join(opciones.getAddonInfo('path'),'resources/imagenes/noti_informa.png')
notimail = os.path.join(opciones.getAddonInfo('path'),'resources/imagenes/noti_mail.png')

def Notificaciones(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def check_login(source,username):
    logged_in_string = 'Desconectarse'
    unmensaje = '\<strong\>1\</strong\>\smensaje\ssin\sleer'
    dosmensajes = '\<strong\>2\</strong\>\smensajes\ssin\sleer'
    tresmensajes = '\<strong\>3\</strong\>\smensajes\ssin\sleer'
    cuatromensajes = '\<strong\>4\</strong\>\smensajes\ssin\sleer'
    masdecuatro = '\<strong\>5\</strong\>\smensajes\ssin\sleer'
    notienes = 'No tienes mensajes nuevos'
    #print source
    if re.search(logged_in_string,source,re.IGNORECASE):
        if NotiActiva == 'false':
            Notificaciones('Bienvenido de nuevo',username+' , disfruta como siempre','4000',notimail)
            if re.search(unmensaje,source,re.IGNORECASE):
                Notificaciones('Mensajes Privados','Tienes 1 MP sin leer','4000',notimail)
            elif re.search(dosmensajes,source,re.IGNORECASE):
                Notificaciones('Mensajes Privados','Tienes 2 MPs sin leer','4000',notimail)
            elif re.search(tresmensajes,source,re.IGNORECASE):
                Notificaciones('Mensajes Privados','Tienes 3 MPs sin leer','4000',notimail)
            elif re.search(cuatromensajes,source,re.IGNORECASE):
                Notificaciones('Mensajes Privados','Tienes 4 MPs sin leer','4000',notimail)
            elif re.search(masdecuatro,source,re.IGNORECASE):
                Notificaciones('Mensajes Privados','Tienes 5 MPs o mas sin leer','4000',notimail)
            else:
                Notificaciones('Mensajes Privados',notienes,'4000',notimail)

        return True
    else:
        return False
	
def doLogin(cookiepath, username, password):

    if not os.path.isfile(cookiepath):
        cookiepath = os.path.join(cookiepath,'cookies.lwp')
        
    try:
        os.remove(cookiepath)
    except:
        pass

    if username and password:
        login_url = 'http://xbmcspain.com/foro/ucp.php?mode=login&redirect=.%2Findex.php'

        header_string = 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'

        login_data = urllib.urlencode({'username':username, 'password':password, 'autologin':1, 'viewonline':0, 'login':'Identificarse'})

        req = urllib2.Request(login_url, login_data)
        req.add_header('User-Agent',header_string)

        cj = cookielib.LWPCookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        response = opener.open(req)
        source = response.read()
        response.close()

        login = check_login(source,username)

        if login == True:
            cj.save(cookiepath)

        return login
		
		
    
    else:
        return False