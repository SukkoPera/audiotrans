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

from AudioTrans.Encoder import Encoder
from AudioTrans.Endianness import Endianness
from AudioTrans.Quality import Quality
from AudioTrans.AudioTag import AudioTag

class EncFlac (Encoder):
	name = "Official FLAC encoder"
	version = "0.1"
	supportedExtensions = ["flac"]
	executable = "flac"
	endianness = Endianness.LITTLE
	parametersRaw = ["--force-raw-format", "--endian=little", "--channels=2", "--bps=16", "--sample-rate=44100", "--sign=unsigned"]
	parametersLQ = ["--fast", "-f", "-", "-o"]
	parametersMQ = ["-5", "-f", "-", "-o"]
	parametersHQ = ["--best", "-f", "-", "-o"]
	defaultQuality = Quality.HIGH

if __name__ == '__main__':
	encFact = EncFlac ()
	enc = encFact.getDefaultEncoder ("test.flac")
	enc.write ("*" * 1000)
	enc.close ()
