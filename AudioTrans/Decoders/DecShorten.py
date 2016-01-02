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

from AudioTrans.Decoder import Decoder
from AudioTrans.Endianness import Endianness
from AudioTrans.Quality import Quality
from AudioTrans.AudioTag import AudioTag

class DecShorten (Decoder):
	name = "Official Shorten decoder"
	version = "20160101"
	supportedExtensions = ["shn"]
	executable = "shorten"
	endianness = Endianness.LITTLE
	parameters = ["-x", "#INFILE#", "-"]

	def _makeCmdLine (self):
		assert (self.filename is not None and self.filename != "")
		self.cmdLine = [self.__class__.executablePath]
		self.cmdLine.extend (self.parameters)
		self.cmdLine = [self.filename if x == "#INFILE#" else x for x in self.cmdLine]
		return self.cmdLine

	def getTag (self):
		# Shorten does not seem to support tags
		raise SyntaxError

if __name__ == '__main__':
	decFact = DecShorten ()
	dec = decFact.getDefaultDecoder ("src.shn")
	buf = dec.read (1000)
	print buf
	dec.close ()
