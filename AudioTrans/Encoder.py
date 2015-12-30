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

from BaseCoder import BaseCoder, CoderException
import Process


class Encoder (BaseCoder):
	# True if decoder requires raw input
	rawInput = False

	def __init__ (self, filename, quality):
		super (Encoder, self).__init__ ()
		self.filename = filename
		if quality is None:
			self.quality = self.defaultQuality
		else:
			self.quality = quality

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

