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

import os
import subprocess

class ProcessException (Exception):
	pass

class Process (object):
	"""Base class for runnable objects."""
	def __init__ (self, cmdLine, debug = 1):
		"""Starts the process and returns a pipe to it."""
		self._cmdLine = cmdLine
		self._debug = debug
		if debug:
			print "Starting process: %s" % " ".join (self._cmdLine)
		self.process = subprocess.Popen (self._cmdLine, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 1, close_fds = True)
		if debug:
			print "Process started successfully, pid = %d" % self.process.pid

	def close (self):
		assert (self.process)
		self.process.stdin.close ()
		self.process.stdout.close ()
		ret = self.process.wait ()
		if ret != 0:
			raise ProcessException ("ERROR: Process returned %d" % ret)
		elif self._debug:
			print "Process terminated correctly"

		return ret


class DecoderProcess (Process):
	def __init__ (self, cmdLine):
		super (DecoderProcess, self).__init__ (cmdLine)

	def read (self, size):
		assert (self.process)
		return self.process.stdout.read (size)

#	def preClose (self):
#		self.process.stdin.close ()


class EncoderProcess (Process):
	def __init__ (self, cmdLine):
		super (EncoderProcess, self).__init__ (cmdLine)

	def write (self, str):
		assert (self.process)
		self.process.stdin.write (str)

#	def preClose (self):
#		self.process.stdout.close ()
