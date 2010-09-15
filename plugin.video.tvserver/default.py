"""
    Plugin for streaming live TV to XBMC from TVServer
"""

# main imports
import sys

# plugin constants
__plugin__ = "TVServer Live TV"
__author__ = "evildude aka prashantv"
__url__ = "http://www.scintilla.utwente.nl/~marcelg/"
__svn_url__ = ""
__credits__ = "margro, Prashant V"
__version__ = "1.1.0.75"


if ( __name__ == "__main__" ):
    from MpTv import xbmcplugin_list as plugin
    plugin.Main()
