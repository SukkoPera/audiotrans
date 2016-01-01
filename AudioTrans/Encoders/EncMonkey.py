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

from mutagen.monkeysaudio import MonkeysAudio as mutaMAC


# WARNING: The stock "mac" doesn't allow reading from stdin, a patched version is necessary.
# See http://www.etree.org/shnutils/shntool/
class EncMonkey (Encoder):
	name = "Official Monkey's Audio encoder"
	version = "20160101"
	supportedExtensions = ["ape"]
	executable = "mac"
	endianness = Endianness.LITTLE
	parametersLQ = ["-", "DUMMY", "-c1000"]
	parametersMQ = ["-", "DUMMY", "-c2000"]
	parametersHQ = ["-", "DUMMY", "-c5000"]
	defaultQuality = Quality.MEDIUM

	# Filename must not be appended with mac
	def _makeCmdLine (self):
		assert (self.filename and self.filename != "")
		self.cmdLine = [self.executablePath]
		parameters = self._getQualityParameters ()
		parameters[1] = self.filename
		self.cmdLine.extend (parameters)
		return self.cmdLine

	def setTag (self, tag):
		audio = mutaMAC (self.filename)
		if tag.artist is not None:
			audio["artist"] = tag.artist
		if tag.album is not None:
			audio["album"] = tag.album
		if tag.title is not None:
			audio["title"] = tag.title
		if tag.year is not None:
			audio["date"] = tag.year
		if tag.comment is not None:
			audio["comment"] = tag.comment
		if tag.trackNo is not None:
			audio["tracknumber"] = tag.trackNo
		if tag.genre is not None:
			audio["genre"] = tag.genre
		audio.save ()

if __name__ == '__main__':
	encFact = EncMonkey ()
	enc = encFact.getDefaultEncoder ("test.ape")
	enc.write ("*" * 1000)
	enc.close ()
