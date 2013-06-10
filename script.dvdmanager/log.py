#Standard modules
import inspect
import time

"""Basic error logging functionality for the project"""

"""
Description:
	Used to display non-critical messages
Args:
	message::string : text to be displayed
"""
def debug( message ):
	_log( "debug", message )

"""
Description:
	Used to display non-critical messages
Args:
	message::string : text to be displayed
"""
def error( message ):
	_log( "error", message )
	
"""
Description:
	Used internally to display all messages
Args:
	level::string : severity of the issue
	message::string : text to be displayed
"""
def _log( level, message ):
	caller = inspect.stack()[ 3 ][ 3 ]
	line = time.strftime( "%Y.%m.%d %H:%M:%S" ) + " (" + level + ") : " + caller + " : " + message
	print line