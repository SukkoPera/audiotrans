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

from BaseCoder import BaseCoder, MissingCoderExe
import Process
#import Quality


class EncoderFactory (BaseCoder):
	def __init__ (self):
		super (EncoderFactory, self).__init__ ()
		print "Using \"%s\" as \"%s\" encoder" % (self.executablePath, "/".join (self.supportedExtensions))


	def getEncoder (self, outFilename, quality = None):
		try:
			if quality is None:
				quality = self.defaultQuality
			argv = self.makeCmdLine (outFilename, quality)
			enc = Process.EncoderProcess (argv)
			return enc, self.endianness
		except Exception, ex:
			print "Exception in getEncoder(): %s" % ex.message
			raise

	#def __del__ (self):
		#print "Encoder for \"%s\" being destroyed!" % self.outfileext

