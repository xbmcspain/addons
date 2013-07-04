#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xbmc, xbmcgui, os, sys, xbmcplugin, xbmcaddon
import urllib, urllib2, cookielib
from resources.lib.main import main

Opciones = xbmcaddon.Addon()
Favo = os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'resources/Favoritos.xml')
Favoritoss = "file://"+Favo

BASE=[
('http://playstationstorelibre.eshost.es/ps/Espana.xml', 'España'),
('http://xbmcspain.com/foro/Espana.xml', 'España XBMCERO'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Series.xml', 'Series'),
(Favoritoss, 'Favoritos'),
]
BASE1=[
('http://xbmcspain.com/foro/Espana.xml', 'España'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Series.xml', 'Series'),
('http://xbmcspain.com/foro/+18.xml', 'Adultos'),
(Favoritoss, 'Favoritos'),
]
BASE2=[
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Espana.xml', 'España'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Series.xml', 'Series'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/USA.xml', 'EE.UU.'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Romania.xml', 'Rumanía'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Portugal.xml', 'Portugal'),
(Favoritoss, 'Favoritos'),
]
BASE3=[
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Espana.xml', 'España'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Series.xml', 'Series'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/+18.xml', 'Adultos'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/USA.xml', 'EE.UU.'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Romania.xml', 'Rumanía'),
('https://raw.github.com/xbmcspain/addons/master/plugin.video.rtmpGUIplus/resources/canales/Portugal.xml', 'Portugal'),
(Favoritoss, 'Favoritos'),
]
BASE4=[
('http://playstationstorelibre.eshost.es/ps/Espana.xml', 'España 2'),
('https://dl.dropbox.com/s/doa8gt9s0tdo2y7/Espana.xml', 'España 3'),
('http://playstationstorelibre.eshost.es/ps/Series.xml', 'Series 2'),
(Favoritoss, 'Favoritos'),
]
BASE5=[
('http://playstationstorelibre.eshost.es/ps/Espana.xml', 'España 2'),
('https://dl.dropbox.com/s/doa8gt9s0tdo2y7/Espana.xml', 'España 3'),
('http://playstationstorelibre.eshost.es/ps/Series.xml', 'Series 2'),
('http://playstationstorelibre.eshost.es/ps/Romania.xml', 'Rumanía 2'),
('http://playstationstorelibre.eshost.es/ps/USA.xml', 'EE.UU. 2'),
('http://playstationstorelibre.eshost.es/ps/Romania.xml', 'Rumanía 2'),
('http://playstationstorelibre.eshost.es/ps/Portugal.xml', 'Portugal 2'),
(Favoritoss, 'Favoritos'),
]
BASE6=[
('http://playstationstorelibre.eshost.es/ps/Espana.xml', 'España 2'),
('https://dl.dropbox.com/s/doa8gt9s0tdo2y7/Espana.xml', 'España 3'),
('http://playstationstorelibre.eshost.es/ps/Series.xml', 'Series 2'),
('http://playstationstorelibre.eshost.es/ps/Romania.xml', 'Rumanía 2'),
('http://playstationstorelibre.eshost.es/ps/USA.xml', 'EE.UU. 2'),
('http://playstationstorelibre.eshost.es/ps/Romania.xml', 'Rumanía 2'),
('http://playstationstorelibre.eshost.es/ps/Portugal.xml', 'Portugal 2'),
('http://playstationstorelibre.eshost.es/ps/+18.xml', 'Adultos 2'),
(Favoritoss, 'Favoritos'),
]
if (Opciones.getSetting("habilitarmodoadultos") == 'true') and (Opciones.getSetting("canalesinternacionales") == 'true') and (Opciones.getSetting("habilitarespaldo") == 'true'): from resources.lib.main import main;main(BASE6)
if (Opciones.getSetting("habilitarmodoadultos") == 'false') and (Opciones.getSetting("canalesinternacionales") == 'true') and (Opciones.getSetting("habilitarespaldo") == 'true'): from resources.lib.main import main;main(BASE5)
if (Opciones.getSetting("habilitarmodoadultos") == 'false') and (Opciones.getSetting("canalesinternacionales") == 'false') and (Opciones.getSetting("habilitarespaldo") == 'true'): from resources.lib.main import main;main(BASE4)
if (Opciones.getSetting("habilitarmodoadultos") == 'true') and (Opciones.getSetting("canalesinternacionales") == 'true') and (Opciones.getSetting("habilitarespaldo") == 'false'): from resources.lib.main import main;main(BASE3)
if (Opciones.getSetting("habilitarmodoadultos") == 'false') and (Opciones.getSetting("canalesinternacionales") == 'true') and (Opciones.getSetting("habilitarespaldo") == 'false'): from resources.lib.main import main;main(BASE2)
if (Opciones.getSetting("habilitarmodoadultos") == 'true') and (Opciones.getSetting("canalesinternacionales") == 'false') and (Opciones.getSetting("habilitarespaldo") == 'false'): from resources.lib.main import main;main(BASE1)
else: from resources.lib.main import main;main(BASE)
