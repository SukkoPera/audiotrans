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

from AudioTrans.Decoder import Decoder
from AudioTrans.Endianness import Endianness
from AudioTrans.Quality import Quality
from AudioTrans.AudioTag import AudioTag

import mutagen
from mutagen.easyid3 import EasyID3

class DecMadplay (Decoder):
	name = "Madplay MP3 decoder"
	version = "20160101"
	supportedExtensions = ["mp3"]
	executable = "madplay"
	endianness = Endianness.LITTLE
	parameters = ["-Q", "-owave:-"]

	def getTag (self):
		logger.debug ("Valid ID3 fields: %s", ", ".join (sorted (EasyID3.valid_keys.keys ())))

		try:
			m = EasyID3 (self.filename)
			logger.info ("Available tag fields: %s", m)
			tag = AudioTag ()
			if "artist" in m:
				tag.artist = m["artist"]
			if "album" in m:
				tag.album = m["album"]
			if "title" in m:
				tag.title = m["title"]
			if "date" in m:
				tag.year = m["date"]
			if "comment" in m:
				tag.comment = m["comment"]
			if "tracknumber" in m:
				tag.trackNo = m["tracknumber"]
			if "genre" in m:
				tag.genre = m["genre"]
		except mutagen.id3.ID3NoHeaderError:
			# File is not tagged
			tag = None

		return tag

if __name__ == '__main__':
	decFact = DecMadplay ()
	dec = decFact.getDefaultDecoder ("source.mp3")
	buf = dec.read (1000)
	print buf
	dec.close ()
