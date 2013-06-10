"""
Set up some basic configuration values
TODO: make configurable via UI, once we have one
"""
#Standard modules
import os

ApplicationName = "XBMC DVD Manager"
BatchFileTypeMask = ".txt"
DefaultVideo = "insertDisc.mpg"
DefaultVideoExtension = os.path.splitext( DefaultVideo )[ 1 ][ 1: ]