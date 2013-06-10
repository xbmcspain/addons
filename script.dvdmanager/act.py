#Project modules
import log
import dvd

"""
Description:
	Processes a newline-deliminated list of videos
Args:
	batchFile: name of a newline-deliminated file of titles to be processed
	saveLocation: directory to which all output files are saved
	progress::DialogProgress : used to update the operation's progress
	lang::lang : the currently loaded language object
Returns:
	[0]: number of successes
	[1]: number of failures
	[2]: number of skips
"""
def processBatch( batchFile, saveLocation, progress, lang ):
	try:
		input = open( batchFile, "r" )
	except IOError:
		log.error( "Zero files saved, unable to open the input file: " + batchFile )
		return -1, -1, -1
	
	data = input.read()
	input.close()
	
	names = data.splitlines()
	count = len( names )
	runningTotal = 0
	successes = 0
	failures = 0
	skips = 0
	
	for name in names:
		if progress.iscanceled():
			break
		else:
			runningTotal = runningTotal + 1
			progress.update( runningTotal * 100 / count, lang.get( "Add_Batch_Progress_Status" ).replace( "{0}", str( runningTotal ) ).replace( "{1}", str( count ) ), name )
		if name == "" or name is None:
			skips = skips + 1
			continue
		video = dvd.dvd( saveLocation, name )
		result = video.add()
		if result > 0:
			successes = successes + 1
		elif result < 0:
			failures = failures +1
		else:
			skips = skips + 1
	
	return successes, failures, skips