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

import subprocess
import fcntl
import os

from Module import Module
from Endianness import Endianness


class Filter (Module):
	name = "SoX-based Filter"
	version = "20160102"
	executable = "sox"

	SOX_BUFSIZE = 8192		# 8192 is the default for SoX v14.4.0
	READ_BUFSIZE = 1024 * 32

	def __init__ (self, dec, enc):
		super (Filter, self).__init__ ()
		self._dec = dec
		self._enc = enc
		self._buf = ""
		self._eof = False

	def _realStart (self):
		ret = subprocess.Popen (self._cmdLine, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = self._devnull, bufsize = 0, close_fds = True)
		fl = fcntl.fcntl (ret.stdout, fcntl.F_GETFL)
		fcntl.fcntl (ret.stdout, fcntl.F_SETFL, fl | os.O_NONBLOCK)
		return ret

	def write (self, str):
		assert self.process is not None
		self.process.stdin.write (str)

	def close (self):
		assert self.process is not None
		self.process.stdin.close ()
		self.process.stdout.close ()
		super (Filter, self).close ()

	def _makeCmdLine (self):
		# Start with general options
		self._cmdLine = [self.__class__.executablePath, "--buffer", str (self.SOX_BUFSIZE), "--ignore-length"]

		# Raw input options
		if self._dec.rawOutput:
			logging.info ("Enabling sox filter raw input")
			self._cmdLine += ["-t", "raw", "-r", "44100", "-c", "2", "-b", "16", "-e", "signed-integer", "--endian"]
			if self._dec.endianness == Endianness.LITTLE:
				self._cmdLine += ["little"]
			else:
				self._cmdLine += ["big"]
		else:
			self._cmdLine += ["-t", "wav"]

		# Input filename: stdin
		self._cmdLine += ["-"]

		if self._enc.rawInput:
			logging.info ("Enabling sox filter raw output")
			self._cmdLine += ["-t", "raw", "-r", "44100", "-c", "2", "-b", "16", "-e", "signed-integer", "--endian"]
			if self._enc.endianness == Endianness.LITTLE:
				self._cmdLine += ["little"]
			else:
				self._cmdLine += ["big"]
		else:
			self._cmdLine += ["-t", "wav"]

		# Output filename: stdout
		self._cmdLine += ["-"]

	def _fillBuf (self):
		while not self._eof and len (self._buf) < self.READ_BUFSIZE:
			buf = self._dec.read (self.READ_BUFSIZE)
			if len (buf) == 0:
				logger.debug ("decoder input for sox EOF!")
				self._eof = True
			self._buf += buf

	def read (self, size):
		assert self.process is not None
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
					self._buf = self._buf[l:]
				else:
					logger.debug ("Nothing to write, closing stdin")
					# We may be closing stdin multiple times but it seems ok!
					self.process.stdin.close ()

				logger.debug ("Waiting for %d bytes as sox output", size)
				buf = self.process.stdout.read (size)
				if len (buf) > 0:
					retbuf += buf
					logger.debug ("Got %s bytes" % len (buf))
				else:
					logger.debug ("Sox EOF!")
					break
			except IOError as err:
				logger.debug (str (err))
				if err.errno != 11:	# = "Resource temporarily unavailable", meaning no output is available yet from sox
					raise
		return retbuf

if __name__ == "__main__":
	bs = Filter (None)
