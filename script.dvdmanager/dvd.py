#Standard modules
import os
import shutil
#Project modules
import config
import log

class dvd:
	"""Represents a DVD in your collection"""
	
	"""
	Description:
		basic constructor
		assigns values to instance variables
	Args:
		location: where the file will be saved
		name: the name of video, without file extension
	Returns:
		a new OfflineVideo instance
	"""
	def __init__( self, location, name ):
		self.location = os.path.abspath( location )
		self.name = name

	"""
	Description:
		copies the default video and saves it to the specified path 
	Returns:
		Success: 1
		Skipped: 0
		Failure: -1
	"""
	def add( self ):
		#We need to make sure the location actually exists before we try writing there.
		if not os.path.isdir( self.location ):
			try:
				os.makedirs( self.location )
			except OSError:
				log.error( "Failed to create directory: " + self.location )
				return -1
		
		src = os.path.join( os.getcwd(), config.DefaultVideo )
		dst = self.path()
		
		#We don't want to risk overwriting any existing files, until we have a prompt.
		if not os.path.isfile( dst ):
			try:
				shutil.copyfile( src, dst )
			except shutil.Error:
				log.error( "Source and destination files are the same" )
				return -1
			except IOError:
				log.error( "Destination is not writable" )
				return -1
			else:
				return 1
		else:
			log.debug( "File already exists: " + dst )
			return 0
	
	"""
	Desciption:
		calculates the full pathname of the file
	Returns:
		the full pathname of the file (including extension)
	"""
	def path( self ):
		return os.path.join( self.location, self.name ) + os.path.extsep + config.DefaultVideoExtension