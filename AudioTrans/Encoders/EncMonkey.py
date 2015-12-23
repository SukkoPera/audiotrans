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

from ..Encoder import EncoderFactory
from ..Quality import Quality
from ..Endianness import Endianness

# WARNING: The stock "mac" doesn't allow reading from stdin, a patched version is necessary.
# See http://www.etree.org/shnutils/shntool/

# NOTE: This does not support raw format audio :( - Then I guess it just won't work!

class EncMonkey (EncoderFactory):
	name = "Official Monkey's Audio encoder"
	version = "0.1"
	supportedExtensions = ["ape"]
	executable = "mac"
	endianness = Endianness.LITTLE
	parametersLQ = ["-", "DUMMY", "-c1000"]
	parametersMQ = ["-", "DUMMY", "-c2000"]
	parametersHQ = ["-", "DUMMY", "-c5000"]
	defaultQuality = Quality.MEDIUM

	def makeCmdLine (self, outFilename, quality, raw = True):
		if raw:
			raise Exception ("Encoder does not support raw format")			
		assert (outFilename and outFilename != "")
		parameters = self.getQualityParameters (quality)
		parameters[1] = outFilename
		self.cmdLine = [self.executablePath]
		self.cmdLine.extend (parameters)
		return self.cmdLine

if __name__ == '__main__':
	encFact = EncMonkey ()
	enc = encFact.getDefaultEncoder ("test.ape")
	enc.write ("*" * 1000)
	enc.close ()
