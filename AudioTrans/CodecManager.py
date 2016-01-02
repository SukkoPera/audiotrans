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

import Encoders
import Decoders
from BaseCoder import CoderException
from Quality import Quality


class CodecManager:
	def __init__ (self):
		self._setupEncoders ()
		self._setupDecoders ()

	def _setupEncoders (self):
		self.outputFormats = {}
		for encoder in Encoders.__all__:
			exec ("from AudioTrans.Encoders import %s" % encoder)
			exec ("encoderClass = %s.%s" % (encoder, encoder))
			try:
				encoderClass.check ()
				for fmt in encoderClass.supportedExtensions:
					self.outputFormats[fmt] = encoderClass
			except CoderException as ex:
				# Encoder executable not found, ignore
				pass
			except Exception as ex:
				# Could not init encoder for some other reason
				logger.warning ("Cannot init encoder \"%s\": %s", encoder, str (ex))

	def _setupDecoders (self):
		self.inputFormats = {}
		for decoder in Decoders.__all__:
			exec ("from AudioTrans.Decoders import %s" % decoder)
			exec ("decoderClass = %s.%s" % (decoder, decoder))
			try:
				decoderClass.check ()
				for fmt in decoderClass.supportedExtensions:
					self.inputFormats[fmt] = decoderClass
			except CoderException as ex:
				# Decoder executable not found, ignore
				pass
			except Exception as ex:
				# Could not init decoder for some other reason
				logger.warning ("Cannot init decoder \"%s\": %s", decoder, str (ex))

	def report (self):
		import sys
		print >> sys.stderr, "Decoders"
		print >> sys.stderr, "-" * 80
		for ext, module in self.inputFormats.iteritems ():
			print >> sys.stderr, "%s --> %s" % (ext, module.getName ())

		print >> sys.stderr

		print >> sys.stderr, "Encoders"
		print >> sys.stderr, "-" * 80
		for ext, module in self.outputFormats.iteritems ():
			print >> sys.stderr, "%s --> %s" % (ext, module.getName ())

	def getEncoderForExtension (self, extension):
		if extension in self.outputFormats:
			return self.outputFormats[extension]
		else:
			raise Exception ("No encoder for %s" % extension)

	def getEncoder (self, outFilename, quality = None):
		dummy, dummy, extension = outFilename.rpartition (".")
		if extension == "":
			raise Exception ("No extension in filename")
		else:
			encClass = self.getEncoderForExtension (extension)
			return encClass (outFilename, quality)

	def getDecoderForExtension (self, extension):
		if extension in self.inputFormats:
			return self.inputFormats[extension]
		else:
			raise Exception ("No decoder for \"%s\"" % extension)

	def getDecoder (self, inFilename, quality = None):
		dummy, dummy, extension = inFilename.rpartition (".")
		if extension == "":
			raise Exception ("No extension in filename")
		else:
			decClass = self.getDecoderForExtension (extension)
			return decClass (inFilename)


if __name__ == '__main__':
	cm = CodecManager ()
	cm.report ()

	dec = cm.getDecoder ("src.mp3")
	print dec
