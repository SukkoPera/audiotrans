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

import utility
from Quality import Quality
from Endianness import Endianness

class CoderException (Exception):
	pass

class BaseCoder (object):
	# The following class members *MUST* be overridden by child classes."
	name = None
	version = None
	supportedExtensions = None
	executable = None
	executablePath = None
	endianness = None
	#~ parametersRaw = None
	#~ parametersWave = None

	@classmethod
	def check (cls):
		"""See if the encoder executable can be found in $PATH"""
		try:
			cls.executablePath = utility.findInPath (cls.executable)
			logger.debug ("Using \"%s\" as \"%s\" decoder", cls.executablePath, "/".join (cls.supportedExtensions))
		except utility.NotFoundInPathException:
			raise CoderException ("Cannot find \"%s\" (\"%s\" encoder) in path" % (cls.executable, "/".join (cls.supportedExtensions)))

	def __init__ (self):
		self.process = None

	def getName (self):
		return "%s v%s" % (self.name, self.version)

#	def __makeOutputFilename (self, basename):
#		"""Makes up the destination filename, usually appending the encoder extension to the filename."""
#		self.outfilename = "%s.%s" % (basename, self.outfileext)
#		return (self.outfilename)
