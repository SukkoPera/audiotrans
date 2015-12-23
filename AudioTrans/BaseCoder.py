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

import utility
from Quality import Quality
from Endianness import Endianness

class MissingCoderExe (Exception):
	pass

class BaseCoder:
	# The following members *MUST* be overridden by child classes."
	name = None
	version = None
	supportedExtensions = None
	executable = None
	endianness = None
	parametersRaw = None
	parametersWave = None
	parametersLQ = None
	parametersMQ = None
	parametersHQ = None
	defaultQuality = None


	def __init__ (self):
		# First of all see if the encoder executable can be found in $PATH
		fullExe = utility.findInPath (self.executable)
		self.executablePath = fullExe

	def getName (self):
		return "%s v%s" % (self.name, self.version)

	def getQualityParameters (self, quality):
		if quality == Quality.LOW:
			parameters = self.parametersLQ
		elif quality == Quality.MEDIUM:
			parameters = self.parametersMQ
		elif quality == Quality.HIGH:
			parameters = self.parametersHQ
		else:
			raise Exception ("No parameters available for quality setting \"%\"" % quality)
		return parameters

	def makeCmdLine (self, outFilename, quality, raw = True):
		"""Makes up the encoder command line. This method just appends
		the output filename to the executable and options provided when
		creating the encoder object, if any. If the encoder needs the
		output filename in a different position, then this method must
		be overridden."""

		assert (outFilename and outFilename != "")
		parameters = self.getQualityParameters (quality)
		self.cmdLine = [self.executablePath]
		if raw and self.parametersRaw is not None:
			self.cmdLine.extend (self.parametersRaw)
		else:		# TODO!
			raise Exception ("Encoder does not support raw format")
		self.cmdLine.extend (parameters)
		self.cmdLine.append (outFilename)
		return self.cmdLine
	
	def getSupportedExtensions (self):
		return self.supportedExtensions

#	def __makeOutputFilename (self, basename):
#		"""Makes up the destination filename, usually appending the encoder extension to the filename."""
#		self.outfilename = "%s.%s" % (basename, self.outfileext)
#		return (self.outfilename)
