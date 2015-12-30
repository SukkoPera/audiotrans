#!/usr/bin/env python

###########################################################################
#   Copyright (C) 2008-2016 by SukkoPera                                  #
#   software@sukkology.net                                                #
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 3 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#   This program is distributed in the hope that it will be useful,       #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#   GNU General Public License for more details.                          #
#                                                                         #
#   You should have received a copy of the GNU General Public License     #
#   along with this program; if not, write to the                         #
#   Free Software Foundation, Inc.,                                       #
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
###########################################################################

from Process import FilterProcess

# The sox-based swapper needs this
import utility

# The pure Python swapper needs this
from array import array

class ByteSwapper (FilterProcess):
	"""Here we could rely on sox, but we might also implement this manually..."""
	SOX_EXE = "sox"
	SOX_BUFSIZE = 8192		# 8192 is the default for SoX v14.4.0, must be <= the size that is read()
	READ_BUFSIZE = 1024 * 32

	def __init__ (self, input_, rawin, rawout, debug = False):
		try:
			self.soxpath = utility.findInPath (self.SOX_EXE)
		except utility.NotFoundInPathException as ex:
			print "sox not found in $PATH"

		self.input_ = input_
		self._eof = False
		self.__debug = debug
		if debug:
			print "Starting sox-based ByteSwapper (sox: %s)" % self.soxpath

		# Start with general options
		cmdline = [self.soxpath, "--buffer", str (self.SOX_BUFSIZE)]

		# Raw input options
		if rawin or 0:
			#inputOpts = ["-t", "raw", "-r", "44100", "-c", "2", "-w", "-u"]
			cmdline += ["-t", "raw", "-r", "44100", "-c", "2", "-b", "16", "-e", "signed-integer"]
		else:
			cmdline += ["-t", "wav"]

		# Input filename
		cmdline += ["-"]

		if rawout:
			#outputOpts = ["-t", "raw", "-r", "44100", "-c", "2", "-w", "-u", "-x"]
			cmdline += ["-t", "raw", "-r", "44100", "-c", "2", "-b", "16", "-e", "signed-integer"]

		# Output filename
		cmdline += ["-"]

		#~ print " ".join (cmdline)
		super (ByteSwapper, self).__init__ (cmdline)

		# Read buffer
		self._buf = ""
		self._eof = False

	def _fillBuf (self):
		while not self._eof and len (self._buf) < self.READ_BUFSIZE:
			buf = self.input_.read (self.READ_BUFSIZE)
			if len (buf) == 0:
				#~ print "decoder input for sox EOF!"
				self._eof = True
			self._buf += buf

	def read (self, size):
		assert (self.process)
		retbuf = ""
		while len (retbuf) < size:
			try:
				self._fillBuf ()
				#~ print "Buffer: %d bytes" % (len (self._buf))
				l = min (self.SOX_BUFSIZE, len (self._buf))
				if l > 0:
					#~ print "Writing %d bytes to sox input" % len
					self.process.stdin.write (self._buf[:l])
					self.process.stdin.flush ()		# This is essential!
					#~ if self._eof:
						#~ self.process.stdin.close ()
					self._buf = self._buf[l:]
				#~ else:
					#~ print "Nothing to write!"

				#~ print "Waiting for %d bytes as sox output" % size
				buf = self.process.stdout.read (size)
				if len (buf) > 0:
					retbuf += buf
					#~ print "ok"
				else:
					#~ print "Sox EOF!"
					break
			except IOError as err:
				#~ print str (err)
				pass

		return retbuf

if __name__ == "__main__":
	bs = ByteSwapper (None)
