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

from AudioTrans.Decoder import DecoderFactory
from AudioTrans.Endianness import Endianness
from AudioTrans.Quality import Quality
from AudioTrans.AudioTag import AudioTag

class DecFaad (DecoderFactory):
	name = "Official FAAD2 decoder"
	version = "0.1"
	supportedExtensions = ["mp4", "m4a", "aac"]
	executable = "faad"
	endianness = Endianness.LITTLE
	parametersRaw = ["-f", "2", "-b", "1", "-s", "44100", "-d"]
	parametersHQ = ["-w"]
	defaultQuality = Quality.HIGH

if __name__ == '__main__':
	decFact = DecFaad ()
	dec = decFact.getDefaultDecoder ("src.aac")
	buf = dec.read (1000)
	print buf
	dec.close ()
