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

from Process import DecoderProcess

# The sox-based swapper needs this
import utility

# The pure Python swapper needs this
from array import array

class ByteSwapperSox (DecoderProcess):
	"""Here we could rely on sox, but we might also implement this manually..."""
	SOX_EXE = "sox"
	SOX_BUFSIZE = 4096		# 8192 is the default for SoX v14.4.0, must be <= the size that is read()

	def __init__ (self, input_, rawin, rawout, debug = False):
		self.soxpath = utility.findInPath (self.SOX_EXE)
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

		# Input filename
		cmdline += ["-"]

		if rawout:
			#outputOpts = ["-t", "raw", "-r", "44100", "-c", "2", "-w", "-u", "-x"]
			cmdline += ["-t", "raw", "-r", "44100", "-c", "2", "-b", "16", "-e", "signed-integer", "-x"]

		# Output filename
		cmdline += ["-"]

		#~ print " ".join (cmdline)
		DecoderProcess.__init__ (self, cmdline)

	def read (self, size):
		assert (self.process)
		assert size >= self.SOX_BUFSIZE, "Must read() from SoX ByteSwapper at least %d bytes" % self.SOX_BUFSIZE
		# We assume that in order to produce N bytes, we need N bytes
		readbuf = ""
		if not self._eof:
			while len (readbuf) < size:
				buf = self.input_.read (size)
				if len (buf) == 0:
					print "decoder input for sox EOF!"
					self._eof = True
					break
				readbuf += buf
			print "Writing %d bytes to sox input" % len (readbuf)
			self.process.stdin.write (readbuf)
			self.process.stdin.flush ()		# This is essential!
			if self._eof:
				self.process.stdin.close ()
			print "Waiting for sox output"
			retbuf = self.process.stdout.read (1)
			print "ok"
		else:
			retbuf = ""
		return retbuf


class ByteSwapperPurePython (DecoderProcess):
	def __init__ (self, input_, debug = False):
		self.input_ = input_
		self.__debug = debug
		if debug:
			print "Starting pure-Python ByteSwapper"

	# LOL, this works!
	def read (self, size):
		buf = self.input_.read (size)
		arr = array ("H", buf)
		arr.byteswap ()
		return arr.tostring ()

	def close (self):
		if self.__debug:
			print "ByteSwapper terminating"
		return 0


# Here we choose which swapper to use. Both seem to be working fine, and
# of course the pure-Python one would introduce much less overhead. But
# we don't trust it so much, so prefer the SoX one if sox is found on the
# system.
try:
	utility.findInPath (ByteSwapperSox.SOX_EXE)
	ByteSwapper = ByteSwapperSox
except utility.NotFoundInPathException as ex:
	print "sox not found in $PATH"
	#~ ByteSwapper = ByteSwapperPurePython

if __name__ == "__main__":
	bs = ByteSwapper (None)
