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

class EncWav (Encoder):
	name = "sox WAV encoder"
	version = "20151231"
	supportedExtensions = ["wav"]
	executable = "sox"
	endianness = Endianness.LITTLE
	#~ parametersRaw = ["-t", "raw", "-r", "44100", "-c", "2", "-b", "16", "-e", "signed-integer", "-"]
	parametersLQ = ["-", "-t", "wav"]
	parametersMQ = parametersLQ		# Quality is really always the same :)
	parametersHQ = parametersLQ
	defaultQuality = Quality.HIGH

	def setTag (self, tag):
		# WAV does not support tags
		raise SyntaxError

if __name__ == '__main__':
	encFact = EncWav ()
	enc = encFact.getDefaultEncoder ("test.wav")
	enc.write ("*" * 1000)
	enc.close ()
