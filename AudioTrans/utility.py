import os
import sys
import re
import urllib

# Module subprocess was introduced in Python 2.4 (Thanks mat|gentoo)
try:
	import subprocess
except ImportError:
	print "ERROR: You need at least Python 2.4 to run this program :(."

class ImException (Exception):
	pass


class NotFoundInPathException (Exception):
	pass


# Useful function
def findInPath (path):
	"""Find the file named path in sys.path.
	Returns the full path name if found, throws if not found"""

	for dirname in os.environ['PATH'].split (os.path.pathsep):
		possible = os.path.join (dirname, path)
		if os.path.isfile (possible):
			return possible
	
	# Not found
	raise NotFoundInPathException


def runCmdAndWait (cmdLine):
	#print cmdLine
	proc = subprocess.Popen (cmdLine, bufsize = 1, close_fds = True)

	# Wait for command completion		
	ret = proc.wait ()
	if ret != 0:
		print "ERROR: \"%s\" returned %d" % (cmdLine, ret)
	return ret
	
	
def fixPath (path):
	# Take away all illegal characters (I know we are removing some valid chars here, but who cares)
	path = re.sub ("[^ A-Za-z0-9\.,'_-]", "-", path)
	# When subbing multibyte charaters, they get replaced by two '-', so strip them down (???)
	path = re.sub ("--", "-", path)
	return path

def escapeForUrl (text):
	return urllib.quote (text)
