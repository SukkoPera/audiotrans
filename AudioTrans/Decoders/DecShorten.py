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

from ..Decoder import DecoderFactory
from ..Quality import Quality
from ..Endianness import Endianness

class DecShorten (DecoderFactory):
	name = "Official Shorten decoder"
	version = "0.1"
	supportedExtensions = ["shn"]
	executable = "shorten"
	endianness = Endianness.LITTLE
	parametersRaw = ["-c", "2", "-t", "u16hl"]
	parametersHQ = ["-x", "-"]
	defaultQuality = Quality.HIGH

if __name__ == '__main__':
	decFact = DecShorten ()
	dec = decFact.getDefaultDecoder ("src.shn")
	buf = dec.read (1000)
	print buf
	dec.close ()
