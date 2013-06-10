#Standard modules
import os
import sys
import xml.dom.minidom
#Third-party modules
import xbmc
#Project modules
import log

class lang:
	"""Handles all of the user facing text and i18n
	Public attributes:
		language::string
	Public methods:
		get( key::string )::string
	"""	
	
	"""
	Description:
		Initializes the strings used for user-facing text
		Attempts to use the system's language, if available
		Falls back to English if the native language is unavailable
	Args:
		rootDir : string : the script's root directory
	"""
	def __init__( self ):
		self.rootDir = os.getcwd()
		self.defaultLanguage = "english"
		self.language = None
		self.file = None
		self.strings = { }
		self.initSupportedLanguage()
		if self.language is not None:
			self.load()
	
	"""
	Description:
		Retrieves the string represented by the provided key
	Args:
		key::string : represents the string to be retrieved
	Returns:
		string : the corresponding value
	"""
	def get( self, key ):
		return self.strings.get( key )
	
	"""
	Description:
		Attempts to use the system's language, if available
		Falls back to English if the native language is unavailable
	Returns:
		self
	TODO:
		we need an elegant way to bail out if a language file cannot be located (program is unusable)
	"""
	def initSupportedLanguage( self ):
		if not self.set( xbmc.getLanguage().lower() ):
			if not self.set( self.defaultLanguage ):
				self.set( None )
				log.error( "Unable to load the default language file: " + self.defaultLanguage )
		return self
	
	"""
	Description:
		determines whether or not the current language is supported
	Returns:
		boolean : whether or not the current language is supported
	"""
	def isSupported( self ):
		return self.language is not None and os.path.isfile( self.file )

	"""
	Description:
		loads the object's language file and all corresponding strings
	Returns:
		self
	TODO:
		we need an elegant way to bail out if a language file cannot be located (program is unusable)
	"""
	def load( self ):
		doc = xml.dom.minidom.parse( self.file )
		root = doc.documentElement
		if ( not root or root.tagName != "strings" ):
			self.set( None )
			log.error( "Unable to parse the language file: " + self.language )
		strings = root.getElementsByTagName( "string" )
		for string in strings:
			key = string.getAttribute( "key" )
			if ( key not in self.strings and string.hasChildNodes() ):
				self.strings[ key ] = string.firstChild.nodeValue
		try:
			doc.unlink()
		except:
			log.debug( "Unable to unlink the language file" )
		return self
	
	"""
	Description:
		Stores the specified language name internally
		Calculates and stores the language file path
	Args:
		language::string : name of the language
	Returns:
		boolean : whether or not the language is supported
	"""
	def set( self, language ):
		self.language = language
		
		if language is None:
			self.file = None
			return False
		else:
			self.file = self.theFile( language )
			return self.isSupported()

	"""
	Description:
		calculates the path of the specified language file
	Args:
		language::string : name of the language file to be calculated
	Returns:
		string : absolute path of the language file
	"""
	def theFile( self, language ):
		return os.path.join( self.rootDir, "language", language, "strings.xml" )