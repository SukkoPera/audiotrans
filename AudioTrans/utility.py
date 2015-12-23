import os
import re
import urllib

class NotFoundInPathException (Exception):
	pass

# Useful function
def findInPath (exe):
	"""Find the file named exe in the system path.
	Returns the full path name if found, throws if not found"""

	for dirname in os.environ['PATH'].split (os.path.pathsep):
		possible = os.path.join (dirname, exe)
		if os.path.isfile (possible):
			return possible

	# Not found
	raise NotFoundInPathException

def fixPath (path):
	# Take away all illegal characters (I know we are removing some valid chars here, but who cares)
	path = re.sub ("[^ A-Za-z0-9\.,'_-]", "-", path)
	# When subbing multibyte charaters, they get replaced by two '-', so strip them down (???)
	path = re.sub ("--", "-", path)
	return path

def escapeForUrl (text):
	return urllib.quote (text)
