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

import Encoders
import Decoders
from BaseCoder import MissingCoderExe
from Quality import Quality


class CodecManager:
	def __init__ (self):
		self.__setupEncoders ()
		self.__setupDecoders ()

	def __setupEncoders (self):
		self.__supportedOutputFormats = {}
		for encoder in Encoders.__all__:
			try:
				exec ("import Encoders.%s" % encoder)
				exec ("encoderModule = Encoders.%s" % encoder)
				exec ("encoderInstance = encoderModule.%s ()" % encoder)
				for format in encoderInstance.getSupportedExtensions ():
					self.__supportedOutputFormats[format] = encoderInstance
			except MissingCoderExe as ex:
				# Encoder executable not found, ignore
				pass
			except Exception as ex:
				# Could not init encoder for some other reason
				print "Cannot init encoder \"%s\": %s" % (encoder, str (ex))

	def __setupDecoders (self):
		self.__supportedInputFormats = {}
		for decoder in Decoders.__all__:
			try:
				exec ("import Decoders.%s" % decoder)
				exec ("decoderModule = Decoders.%s" % decoder)
				exec ("decoderInstance = decoderModule.%s ()" % decoder)
				for format in decoderInstance.getSupportedExtensions ():
					self.__supportedInputFormats[format] = decoderInstance
			except MissingCoderExe as ex:
				# Decoder executable not found, ignore
				pass
			except Exception as ex:
				# Could not init decoder for some other reason
				print "Cannot init decoder \"%s\": %s" % (decoder, str (ex))

	def report (self):
		print >> sys.stderr, "Decoders"
		print >> sys.stderr, "-" * 80
		for ext, module in self.__supportedInputFormats.iteritems ():
			print >> sys.stderr, "%s --> %s" % (ext, module.getName ())

		print >> sys.stderr
		
		print >> sys.stderr, "Encoders"
		print >> sys.stderr, "-" * 80
		for ext, module in self.__supportedOutputFormats.iteritems ():
			print >> sys.stderr, "%s --> %s" % (ext, module.getName ())

	def getAllSupportedOutputFormats (self):
		return self.__supportedOutputFormats

	def getAllSupportedInputFormats (self):
		return self.__supportedInputFormats

	def getEncoderFactory (self, extension):
		if extension in self.__supportedOutputFormats:
			return self.__supportedOutputFormats[extension]
		else:
			raise Exception ("No encoder for %s" % extension)

	def getEncoder (self, outFilename, quality = None):
		dummy, dummy, extension = outFilename.rpartition (".")
		if extension == "":
			raise Exception ("No extension in filename")
		else:
			decFact = self.getEncoderFactory (extension)
			return decFact.getEncoder (outFilename, quality)

	def getDecoderFactory (self, extension):
		if extension in self.__supportedInputFormats:
			return self.__supportedInputFormats[extension]
		else:
			raise Exception ("No decoder for \"%s\"" % extension)

	def getDecoder (self, inFilename, quality = None):
		dummy, dummy, extension = inFilename.rpartition (".")
		if extension == "":
			raise Exception ("No extension in filename")
		else:
			decFact = self.getDecoderFactory (extension)
			return decFact.getDecoder (inFilename, quality)


if __name__ == '__main__':
	cm = CodecManager ()
	cm.report ()

	dec = cm.getDecoder ("src.mp3")
	print dec
