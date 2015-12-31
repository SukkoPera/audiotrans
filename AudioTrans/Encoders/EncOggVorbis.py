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

from mutagen.oggvorbis import OggVorbis as mutaOggVorbis

class EncOggVorbis (Encoder):
	name = "Official OGG Vorbis encoder"
	version = "20151231"
	supportedExtensions = ["ogg"]
	executable = "oggenc"
	endianness = Endianness.LITTLE
	parametersCommon = ["--quiet"]
	parametersLQ = parametersCommon + ["-q", "1", "-", "-o"]
	parametersMQ = parametersCommon + ["-q", "3", "-", "-o"]
	parametersHQ = parametersCommon + ["-q", "6", "-", "-o"]
	defaultQuality = Quality.MEDIUM

	def setTag (self, tag):
		audio = mutaOggVorbis (self.filename)
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
	# This won't work as encoder expects valid wav data
	logging.basicConfig (level = logging.DEBUG)
	EncOggVorbis.check ()
	encFact = EncOggVorbis ("test.ogg", Quality.MEDIUM)
	enc = encFact.getProcess ()
	enc.write ("*" * 1000)
	enc.close ()

	tag = AudioTag ()
	tag.artist = "artist"
	tag.album = "album"
	encFact.setTag (tag)
