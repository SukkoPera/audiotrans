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

from BaseCoder import BaseCoder, MissingCoderExe
import Process


class DecoderFactory (BaseCoder):
	def __init__ (self):
		try:
			super (DecoderFactory, self).__init__ ()
			print "Using \"%s\" as \"%s\" decoder" % (self.executablePath, "/".join (self.supportedExtensions))
		except:
			raise MissingCoderExe ("Cannot find \"%s\" (\"%s\" decoder) in path" % (self.executable, "/".join (self.supportedExtensions)))

	def _makeCmdLine (self, filename, raw = False):
		assert (filename is not None and filename != "")
		self.cmdLine = [self.executablePath]
		if raw:
			assert self.parametersRaw is not None
			self.cmdLine.extend (self.parametersRaw)
		self.cmdLine.extend (self.parameters)
		self.cmdLine.append (filename)
		return self.cmdLine

	def getDecoder (self, inFilename, quality = None):
		try:
			if quality is None:
				quality = self.defaultQuality
			argv = self._makeCmdLine (inFilename)
			dec = Process.DecoderProcess (argv)
			#print dec.process.stdout.readlines ()
			return dec, self.endianness
		except Exception, ex:
			print "Exception in getDecoder(): %s" % ex.message
			raise
