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


class DecoderFactory (BaseCoder):
	# True if decoder only produces raw output
	rawOutput = False

	def __init__ (self, filename):
		super (DecoderFactory, self).__init__ ()
		self.filename = filename

	def _makeCmdLine (self, raw = False):
		assert (self.filename is not None and self.filename != "")
		self.cmdLine = [self.__class__.executablePath]
		if raw:
			assert self.parametersRaw is not None
			self.cmdLine.extend (self.parametersRaw)
		self.cmdLine.extend (self.parameters)
		self.cmdLine.append (self.filename)
		return self.cmdLine

	def getProcess (self):
		if self.process is None:
			try:
				self.process = Process.DecoderProcess (self._makeCmdLine ())
			except Exception, ex:
				logger.exception ("Exception in getDecoder(): %s", str (ex))
				raise
		return self.process

	def getTag (self):
		raise NotImplementedError
