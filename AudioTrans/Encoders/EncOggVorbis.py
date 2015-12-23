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

class EncOggVorbis (EncoderFactory):
	name = "Official OGG Vorbis encoder"
	version = "0.1"
	supportedExtensions = ["ogg"]
	executable = "oggenc"
	endianness = Endianness.LITTLE
	parametersRaw = ["--raw", "--raw-rate=44100", "--raw-chan=2", "--raw-bits=16", "--raw-endianness=0"]		# 0 is little-endian
	parametersLQ = ["-q", "1", "-", "-o"]
	parametersMQ = ["-q", "3", "-", "-o"]
	parametersHQ = ["-q", "6", "-", "-o"]
	defaultQuality = Quality.MEDIUM

if __name__ == '__main__':
	encFact = EncOggVorbis ()
	enc = encFact.getDefaultEncoder ("test.ogg")
	enc.write ("*" * 1000)
	enc.close ()
