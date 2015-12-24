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

from AudioTrans.Encoder import EncoderFactory
from AudioTrans.Endianness import Endianness
from AudioTrans.Quality import Quality

class EncLame (EncoderFactory):
	name = "LAME MP3 encoder"
	version = "0.1"
	supportedExtensions = ["mp3"]
	executable = "lame"
	endianness = Endianness.LITTLE
	parametersRaw = ["-r", "-s", "44100", "--bitwidth", "16"]
	parametersLQ = ["--alt-preset", "128", "-"]
	parametersMQ = ["--alt-preset", "160", "-"]
	parametersHQ = ["--preset", "extreme", "-B", "192", "-b", "96", "-"]
	defaultQuality = Quality.MEDIUM

	#~ def __init__ (self):
		#~ super (EncLame, self).__init__ (self)

#	def __makeCmdLine (self):
#		tmp = EncoderFactory.__makeCmdLine (self)
#		if self.title:
#			tmp.extend (["--tt", self.title])
#		if self.artist:
#			tmp.extend (["--ta", self.artist])
#		if self.album:
#			tmp.extend (["--tl", self.album])
#		if self.year:
#			tmp.extend (["--ty", self.year])
#		if self.trackNo:
#			tmp.extend (["--tn", `self.trackNo`])
#		if self.genre:
#			tmp.extend (["--tg", self.genre])
#		if self.comment:
#			tmp.extend (["--tc", self.comment])
#		tmp.append ("--id3v1-only")
#		self.cmdLine = tmp
#		return tmp


if __name__ == '__main__':
	encFact = EncLame ()
	enc = encFact.getDefaultEncoder ("test.mp3")
	enc.write ("*" * 1000)
	enc.close ()

