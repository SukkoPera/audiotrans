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

import os
import subprocess

import utility
from Quality import Quality
from Endianness import Endianness



class CoderException (Exception):
	pass

class Module (object):
	# The following class members *MUST* be overridden by child classes
	name = None
	version = None
	executable = None
	executablePath = None

	"""Base class for runnable objects."""
	def __init__ (self):
		if self.__class__.executablePath is None:
			self.__class__.check ()
		self._cmdLine = None
		self.process = None
		self._devnull = open (os.devnull)

	@classmethod
	def getName (cls):
		return "%s v%s" % (cls.name, cls.version)

	def start (self):
		"""Starts the process and sets up pipes to/from it."""
		if self._cmdLine is None:
			self._makeCmdLine ()
		assert self._cmdLine is not None
		logger.info ("Starting process: %s" % " ".join (self._cmdLine))
		self.process = self._realStart ()
		logger.info ("Process started successfully, pid = %d", self.process.pid)

	def close (self):
		assert self.process is not None
		ret = self.process.wait ()
		if ret != 0:
			logger.error ("Process returned %d", ret)
			raise ProcessException ("ERROR: Process returned %d" % ret)
		else:
			logger.info ("Process terminated correctly")

		return ret

	# Please override!
	def _realStart (self):
		raise NotImplementedError

	#~ def getProcess (self):
		#~ if self.process is None:
			#~ try:
				#~ self.start ()
			#~ except Exception, ex:
				#~ logger.exception ("Exception in getDecoder(): %s", str (ex))
				#~ raise
		#~ return self.process

	@classmethod
	def check (cls):
		"""See if the encoder executable can be found in $PATH"""
		try:
			cls.executablePath = utility.findInPath (cls.executable)
			logger.debug ("Using \"%s\" for module \"%s\"", cls.executablePath, cls.getName ())
		except utility.NotFoundInPathException:
			raise CoderException ("Cannot find \"%s\" in path for module \"%s\"" % (cls.executable, cls.getName ()))
