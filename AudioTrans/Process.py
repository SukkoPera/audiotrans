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
		self.process = self._start ()
		if debug:
			print "Process started successfully, pid = %d" % self.process.pid

	# Please override!
	def _start (self):
		raise NotImplementedError

	def close (self):
		ret = self.process.wait ()
		if ret != 0:
			raise ProcessException ("ERROR: Process returned %d" % ret)
		elif self._debug:
			print "Process terminated correctly"

		return ret


class DecoderProcess (Process):
	def __init__ (self, cmdLine):
		super (DecoderProcess, self).__init__ (cmdLine)

	def _start (self):
		return subprocess.Popen (self._cmdLine, stdin = open (os.devnull), stdout = subprocess.PIPE, stderr = open (os.devnull), bufsize = 0, close_fds = True)

	def read (self, size):
		assert (self.process)
		return self.process.stdout.read (size)

#	def preClose (self):
#		self.process.stdin.close ()

	def close (self):
		assert (self.process)
		self.process.stdout.close ()
		super (DecoderProcess, self).close ()

class EncoderProcess (Process):
	def __init__ (self, cmdLine):
		super (EncoderProcess, self).__init__ (cmdLine)

	def _start (self):
		return subprocess.Popen (self._cmdLine, stdin = subprocess.PIPE, stdout = open (os.devnull), stderr = open (os.devnull), bufsize = 0, close_fds = True)

	def write (self, str):
		assert (self.process)
		self.process.stdin.write (str)

#	def preClose (self):
#		self.process.stdout.close ()

	def close (self):
		assert (self.process)
		self.process.stdin.close ()
		super (EncoderProcess, self).close ()

import fcntl
class FilterProcess (Process):
	def __init__ (self, cmdLine):
		super (FilterProcess, self).__init__ (cmdLine)

	def _start (self):
		ret = subprocess.Popen (self._cmdLine, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = open (os.devnull), bufsize = 0, close_fds = True)
		fl = fcntl.fcntl (ret.stdout, fcntl.F_GETFL)
		fcntl.fcntl (ret.stdout, fcntl.F_SETFL, fl | os.O_NONBLOCK)
		return ret

	def read (self, size):
		assert (self.process)
		return self.process.stdout.read (size)

	def write (self, str):
		assert (self.process)
		self.process.stdin.write (str)

	def close (self):
		assert (self.process)
		self.process.stdin.close ()
		self.process.stdout.close ()
		super (FilterProcess, self).close ()
