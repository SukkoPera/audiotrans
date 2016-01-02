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

import subprocess

from BaseCoder import BaseCoder
import Process


class Decoder (BaseCoder):
	supportedExtensions = None
	endianness = None
	parameters = None

	# True if decoder only produces raw output
	rawOutput = False

	def __init__ (self, filename):
		super (Decoder, self).__init__ ()
		self.filename = filename

	def _realStart (self):
		return subprocess.Popen (self._cmdLine, stdin = self._devnull, stdout = subprocess.PIPE, stderr = self._devnull, bufsize = 0, close_fds = True)

	def read (self, size):
		assert self.process is not None
		return self.process.stdout.read (size)

	def close (self):
		assert self.process is not None
		self.process.stdout.close ()
		super (Decoder, self).close ()

	def _makeCmdLine (self):
		assert self.filename is not None and self.filename != ""
		self._cmdLine = [self.__class__.executablePath]
		self._cmdLine.extend (self.parameters)
		self._cmdLine.append (self.filename)

	def getTag (self):
		raise NotImplementedError
