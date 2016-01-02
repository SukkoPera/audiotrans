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

from Module import Module
from Quality import Quality

class Encoder (Module):
	supportedExtensions = None
	endianness = None
	parametersLQ = None
	parametersMQ = None
	parametersHQ = None
	defaultQuality = None

	# True if decoder requires raw input
	rawInput = False

	def __init__ (self, filename, quality):
		super (Encoder, self).__init__ ()
		self.filename = filename
		if quality is None:
			self.quality = self.defaultQuality
		else:
			self.quality = quality

	def _realStart (self):
		return subprocess.Popen (self._cmdLine, stdin = subprocess.PIPE, stdout = self._devnull, stderr = self._devnull, bufsize = 0, close_fds = True)

	def write (self, str):
		assert self.process is not None
		self.process.stdin.write (str)

	def close (self):
		assert self.process is not None
		self.process.stdin.close ()
		super (Encoder, self).close ()

	def _getQualityParameters (self):
		if self.quality == Quality.LOW:
			parameters = self.parametersLQ
		elif self.quality == Quality.MEDIUM:
			parameters = self.parametersMQ
		elif self.quality == Quality.HIGH:
			parameters = self.parametersHQ
		else:
			raise Exception ("No parameters available for quality setting \"%\"" % self.quality)
		return parameters

	def _makeCmdLine (self):
		"""Makes up the encoder command line. This method just appends
		the output filename to the executable and options provided when
		creating the encoder object, if any. If the encoder needs the
		output filename in a different position, then this method must
		be overridden."""

		assert self.filename and self.filename != ""
		self._cmdLine = [self.executablePath]
		self._cmdLine.extend (self._getQualityParameters ())
		self._cmdLine.append (self.filename)

	#~ def getProcess (self):
		#~ if self.process is None:
			#~ try:
				#~ self.process = Process.EncoderProcess (self._makeCmdLine ())
			#~ except Exception, ex:
				#~ logger.exception ("Exception in getEncoder(): %s", str (ex))
				#~ raise
		#~ return self.process

	def setTag (self, tag):
		raise NotImplementedError

	#def __del__ (self):
		#print "Encoder for \"%s\" being destroyed!" % self.outfileext

