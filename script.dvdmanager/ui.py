#Standard modules
import os
import traceback
#Third-party modules
import xbmc
import xbmcgui
#Project modules
import act
import config
import lang
import log
import dvd


"""Handles the user interface layer"""

lang = lang.lang()

#http://xbmc.sourceforge.net/python-docs/xbmcgui.html#Dialog-browse
browseTypes = {
	'ShowAndGetDirectory' : 0,
	'ShowAndGetFile' : 1,
	'ShowAndGetImage' : 2,
	'ShowAndGetWriteableDirectory' : 3
}

"""
Description:
	Handles the flow for adding via a batch file
"""
def addBatch():
	fileBrowser = xbmcgui.Dialog()
	file = fileBrowser.browse( 
		browseTypes[ 'ShowAndGetFile' ] #type
		, lang.get( "Add_Batch_Browse_File_Header" ) #heading
		, "files" #shares
		, config.BatchFileTypeMask #mask
		, False #useThumbs
		, False #treatAsFolder
		, os.getcwd() + os.sep #default
	)
	if not os.path.isfile( file ): #the user cancelled the dialog
		return
	location = getSaveLocation( lang.get( "Add_Batch_Browse_Location_Header" ) )
	if location is None:
		return
	progress = xbmcgui.DialogProgress()
	progress.create( lang.get( "Add_Batch_Progress_Header" ) )
	result = act.processBatch( file, location, progress, lang )
	progress.close()
	if result[ 0 ] >= 0 and result[ 1 ] >= 0 and result[ 2 ] >= 0:
		dlg = xbmcgui.Dialog()
		ok( lang.get( "Add_Batch_Results_Header" )
			, lang.get( "Add_Batch_Results_Copied" ).replace( "{0}", str( result[ 0 ] ) )
			, lang.get( "Add_Batch_Results_Failed" ).replace( "{0}", str( result[ 1 ] ) )
			, lang.get( "Add_Batch_Results_Skipped" ).replace( "{0}", str( result[ 2 ] ) ) )

"""
Description:
	Handles the flow for adding a single DVD
"""
def addSingle():
	keyboard = xbmc.Keyboard( "", lang.get( "Add_Single_Input_File_Header" ) )
	keyboard.doModal()
	if not keyboard.isConfirmed():
		return
	location = getSaveLocation( lang.get( "Add_Single_Browse_Location_Header" ) )
	if location is None:
		return
	name = keyboard.getText()
	video = dvd.dvd( location, name )
	status = video.add()
	response = xbmcgui.Dialog()
	if status > 0: #successfully added
		response.ok( lang.get( "Add_Single_Results_Header" ), lang.get( "Add_Single_Results_Success_Info" ), name )
	elif status == 0:
		response.ok( lang.get( "Add_Single_Results_Header" ), lang.get( "Add_Single_Results_Skipped_Info" ), name, lang.get( "Add_Single_Results_Skipped_Footer" ) )
	else:
		response.ok( lang.get( "Add_Single_Results_Header" ), lang.get( "Add_Single_Results_Failure_Info" ), name, lang.get( "Add_Single_Results_Failure_Footer" ) )
	
menuOptions = [ 
		lang.get( "MainMenu_Add_Single" )
		, lang.get( "MainMenu_Add_Batch" )
		, lang.get( "MainMenu_Option_About" )
		, lang.get( "MainMenu_Option_Exit" )
	]
	
"""
Description:
	This is the start of the user flow.
"""
def displayMainMenu():
	menu = xbmcgui.Dialog()
	choice = 0
	while choice >= 0:
		choice = menu.select( config.ApplicationName, menuOptions )
		if choice == 0:
			addSingle()
		elif choice == 1:
			addBatch()
		elif choice == 2:
			about()
		else:
			break
	
"""
Description:
	Displays the "About" dialog
"""
def about():
	dialog = xbmcgui.Dialog()
	dialog.ok( "Half monkey, half zombie, half amazing", "Steven J. Burch", "AsylumFunk.com", "asylumfunk@gmail.com" )

"""
Description:
	Shortcut method for prompting the user for a directory
Args:
	heading::string : File browser heading
Returns:
	Success : the selected location
	Failure : None
"""
def getSaveLocation( heading ):
	locationBrowser = xbmcgui.Dialog()
	location = locationBrowser.browse( 
		browseTypes[ 'ShowAndGetDirectory' ] #type
		,  heading #heading
		, "video" #shares
		, "" #mask
		, True #useThumbs
		, False #treatAsFolder
		, "" #default
	)
	location = os.path.normpath( location )
	if os.path.isdir( location ): #the user selected a location
		return location
	else:
		return None

"""
Description:
	Shortcut method for displaying an OK prompt
Args:
	header::string : dialog title
	line1::string : the first line of text (optional)
	line2::string : the second line of text (optional)
	line3::string : the third line of text (optional)
Returns:
	boolean : whether or not the user clicked OK
"""
def ok( header, line1 = "", line2 = "", line3 = "" ):
	dialog = xbmcgui.Dialog()
	return dialog.ok( header, line1, line2, line3 )