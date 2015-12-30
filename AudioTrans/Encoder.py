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

from BaseCoder import BaseCoder, MissingCoderExe
import Process
#import Quality


class EncoderFactory (BaseCoder):
	def __init__ (self, filename, quality):
		try:
			super (EncoderFactory, self).__init__ ()
			logging.debug ("Using \"%s\" as \"%s\" encoder", self.executablePath, "/".join (self.supportedExtensions))

			self.filename = filename

			if quality is None:
				self.quality = self.defaultQuality
			else:
				self.quality = quality
		except:
			raise MissingCoderExe ("Cannot find \"%s\" (\"%s\" decoder) in path" % (self.executable, "/".join (self.supportedExtensions)))

	def getProcess (self):
		if self.process is None:
			try:
				self.process = Process.EncoderProcess (self.makeCmdLine (self.filename, self.quality))
			except Exception, ex:
				logger.exception ("Exception in getEncoder(): %s", str (ex))
				raise
		return self.process

	def setTag (self, tag):
		raise NotImplementedError

	#def __del__ (self):
		#print "Encoder for \"%s\" being destroyed!" % self.outfileext

