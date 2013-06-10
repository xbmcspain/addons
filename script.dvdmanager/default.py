"""
XBMC DVD Manager
by Steven J. Burch, AsylumFunk.com

For more information, fire up README.txt
To see what's been changing, check out changelog.xml
"""

#Project modules
import ui

if ui.lang.isSupported():
	ui.displayMainMenu()
else:
	ui.ok( "Error", "We were unable to ititialize the script.", "The script will now close.", "If the problem persists, please reinstall the script." )