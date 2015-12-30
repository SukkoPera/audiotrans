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

class EncFaac (Encoder):
	name = "FAAC MPEG-4 encoder"
	version = "0.2"
	supportedExtensions = ["mp4", "m4a", "aac"]
	executable = "faac"
	endianness = Endianness.LITTLE
	parametersRaw = ["-P", "-R", "44100", "-B", "16", "-C", "2", "-X"]
	parametersLQ = ["-w", "-q", "75", "-c", "17000", "-", "-o"]
	parametersMQ = ["-w", "-q", "100", "-c", "18000",  "-", "-o"]
	parametersHQ = ["-w", "-q", "130", "-c", "20000", "-", "-o"]
	defaultQuality = Quality.MEDIUM

if __name__ == '__main__':
	encFact = EncFaac ()
	enc = encFact.getDefaultEncoder ("test.m4a")
	enc.write ("*" * 1000)
	enc.close ()
