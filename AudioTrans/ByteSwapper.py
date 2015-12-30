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

import logging
logger = logging.getLogger (__name__)

from Process import FilterProcess
import utility as utility


class ByteSwapper (FilterProcess):
	SOX_EXE = "sox"
	SOX_BUFSIZE = 8192		# 8192 is the default for SoX v14.4.0
	READ_BUFSIZE = 1024 * 32

	def __init__ (self, dec, enc):
		self.soxpath = utility.findInPath (self.SOX_EXE)

		# Start with general options
		cmdline = [self.soxpath, "--buffer", str (self.SOX_BUFSIZE)]

		# Raw input options
		if 0: #or rawin:
			logging.info ("Enabling sox filter raw input")
			cmdline += ["-t", "raw", "-r", "44100", "-c", "2", "-b", "16", "-e", "signed-integer"]
		else:
			cmdline += ["-t", "wav"]

		# Input filename: stdin
		cmdline += ["-"]

		if enc.rawInput:
			logging.info ("Enabling sox filter raw output")
			cmdline += ["-t", "raw", "-r", "44100", "-c", "2", "-b", "16", "-e", "signed-integer"]

		if enc.endianness != dec.endianness:
			logging.info ("Enabling sox filter endianness change")
			cmdline += ["-x"]

		# Output filename: stdout
		cmdline += ["-"]

		super (ByteSwapper, self).__init__ (cmdline)

		self.input_ = dec.getProcess ()
		#~ self._enc = enc

		# Read buffer
		self._buf = ""
		self._eof = False

	def _fillBuf (self):
		while not self._eof and len (self._buf) < self.READ_BUFSIZE:
			buf = self.input_.read (self.READ_BUFSIZE)
			if len (buf) == 0:
				logger.debug ("decoder input for sox EOF!")
				self._eof = True
			self._buf += buf

	def read (self, size):
		assert (self.process)
		retbuf = ""
		while len (retbuf) < size:
			try:
				self._fillBuf ()
				logger.debug ("Buffer: %d bytes available", len (self._buf))
				l = min (self.SOX_BUFSIZE, len (self._buf))
				if l > 0:
					logger.debug ("Writing %d bytes to sox input", l)
					self.process.stdin.write (self._buf[:l])
					self.process.stdin.flush ()		# This is essential!
					#~ if self._eof:
						#~ self.process.stdin.close ()
					self._buf = self._buf[l:]
				else:
					logger.debug ("Nothing to write!")

				logger.debug ("Waiting for %d bytes as sox output", size)
				buf = self.process.stdout.read (size)
				if len (buf) > 0:
					retbuf += buf
					logger.debug ("OK")
				else:
					logger.debug ("Sox EOF!")
					break
			except IOError as err:
				logger.debug (str (err))
				if err.errno != 11:	# = "Resource temporarily unavailable", meaning no output is available yet from sox
					raise
		return retbuf

if __name__ == "__main__":
	bs = ByteSwapper (None)
