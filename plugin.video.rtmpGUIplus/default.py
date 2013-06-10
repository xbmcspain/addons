#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
__settings__   = xbmcaddon.Addon()

BASE=[
('http://playstationstorelibre.eshost.es/ps/Espana.xml', 'España'),
('https://dl.dropbox.com/s/doa8gt9s0tdo2y7/Espana.xml', 'España Backup'),
]
BASE2=[
('http://playstationstorelibre.eshost.es/ps/Espana.xml', 'España'),
('https://dl.dropbox.com/s/doa8gt9s0tdo2y7/Espana.xml', 'España Backup'),
('http://playstationstorelibre.eshost.es/ps/+18.xml', 'Adultos'),
]
if (__name__ == "__main__") and (__settings__.getSetting("habilitarmodoadultos") == 'true'): from resources.lib.main import main;main(BASE2)
else: from resources.lib.main import main;main(BASE)