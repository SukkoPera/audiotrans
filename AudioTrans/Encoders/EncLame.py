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

import mutagen
from mutagen.easyid3 import EasyID3

class EncLame (Encoder):
	name = "LAME MP3 encoder"
	version = "0.1"
	supportedExtensions = ["mp3"]
	executable = "lame"
	endianness = Endianness.LITTLE
	rawInput = True
	parametersRaw = ["-r", "-s", "44100", "--bitwidth", "16"]
	parametersLQ = ["--alt-preset", "128", "-"]
	parametersMQ = ["--alt-preset", "160", "-"]
	parametersHQ = ["--preset", "extreme", "-B", "192", "-b", "96", "-"]
	defaultQuality = Quality.MEDIUM

	def setTag (self, tag):
		logger.debug ("Valid ID3 fields: %s", ", ".join (sorted (EasyID3.valid_keys.keys ())))

		try:
			audio = EasyID3 (self.filename)
		except mutagen.id3.ID3NoHeaderError:
			audio = mutagen.File (self.filename, easy = True)
			audio.add_tags ()

		audio["artist"] = tag.artist
		audio["album"] = tag.album
		audio["title"] = tag.title
		audio["date"] = tag.year
		#~ audio["comment"] = tag["comment"]
		audio["tracknumber"] = tag.trackNo
		audio["genre"] = tag.genre
		audio.save ()

if __name__ == '__main__':
	logging.basicConfig (level = logging.DEBUG)
	EncLame.check ()
	encFact = EncLame ("test.mp3", Quality.MEDIUM)
	enc = encFact.getProcess ()
	enc.write ("*" * 1000)
	enc.close ()

	tag = AudioTag ()
	tag.artist = "artist"
	tag.album = "album"
	encFact.setTag (tag)
