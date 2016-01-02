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

import sys
import os
import logging

logging.basicConfig (level = logging.INFO)
#~ logger = logging.getLogger (__name__)

from AudioTrans.CodecManager import CodecManager
from AudioTrans.Quality import Quality
from AudioTrans.Filter import Filter

PROGRAM_VERSION = "20151231"
BUFSIZE = 1024 * 8

class ProgressMeter (object):
	sequence = ["|", "/", "-", "\\"]

	def __init__ (self):
		self.stepNo = 0

	def __call__ (self):
		print >> sys.stderr, "\r%s" % self.sequence[self.stepNo % len (self.sequence)],
		sys.stderr.flush ()
		self.stepNo += 1

def transcode (codecsMgr, infile, outfile, quality, overwrite = False, transferTag = True, progressCallback = None):
	assert progressCallback is None or callable (progressCallback)

	print >> sys.stderr, "%s -> %s" % (infile, outfile)
	if os.path.isfile (outfile) and not overwrite:
		print >> sys.stderr, "- Skipping because \"%s\" already exists" % outfile
	else:
		dec = codecsMgr.getDecoder (infile)
		enc = codecsMgr.getEncoder (outfile, quality)
		filt = Filter (dec, enc)

		# Everything is inited, start
		dec.start ()
		enc.start ()
		filt.start ()

		buf = filt.read (BUFSIZE)
		while len (buf) > 0:
			enc.write (buf)
			if progressCallback is not None:
				progressCallback ()
			buf = filt.read (BUFSIZE)

		# Done, close everything
		filt.close ()
		enc.close ()
		dec.close ()

		# Transfer tag
		if transferTag:
			try:
				tag = dec.getTag ()
				if tag is not None:
					#~ print tag
					enc.setTag (tag)
				else:
					print >> sys.stderr, "WARNING: Input file does not contain any tags"
			except NotImplementedError:
				print >> sys.stderr, "ERROR: Cannot transfer tag"
			except SyntaxError:
				print >> sys.stderr, "WARNING: Input or output format does not support tags"

			print "\rTranscoding ended"

def makeOutputFilename (infile, outfile):
	name, separator, extension = outfile.rpartition (".")
	if name == "" and separator == "." and extension != "":
		# Write in current directory by default
		infile = os.path.basename (infile)
		# If outfile is given as ".xxx", change infile's extension to it
		name, dummy, dummy = infile.rpartition (".")
		outfile = "%s.%s" % (name, extension)
	return outfile


from optparse import OptionParser

def welcome ():
	print >> sys.stderr, """----------------------------------------------------------------------
AudioTrans V %s by SukkoPera <software@sukkology.net>
----------------------------------------------------------------------
""" % PROGRAM_VERSION

def main ():
	welcome ()
	cmdline_parser = OptionParser (usage = "usage: %prog [options] -o <output_file> <input file> [<input file> ...]", description = "Audio File Transcoder", version = "%s" % PROGRAM_VERSION)
	# Input and output file options
	cmdline_parser.add_option ("-o", "--output", action = "store", type = "string", dest = "outputFile", help = "File to write to", default = None)
	# Output quality options
	cmdline_parser.add_option ("-L", "--low-quality", action = "store_const", const = Quality.LOW, dest = "output_quality", help = "Low-quality encoding (faster)", default = None)
	cmdline_parser.add_option ("-M", "--medium-quality", action = "store_const", const = Quality.MEDIUM, dest = "output_quality", help = "Medium-quality encoding", default = None)
	cmdline_parser.add_option ("-H", "--high-quality", action = "store_const", const = Quality.HIGH, dest = "output_quality", help = "High-quality encoding (slower)", default = None)
	cmdline_parser.add_option ("-f", "--overwrite", action = "store_true", dest = "overwrite", help = "Overwrite destination file if it exists", default = False)
	(options, args) = cmdline_parser.parse_args ()
	inputFiles = args

	if len (inputFiles) > 0 and options.outputFile and options.outputFile != "":
		# At least an input and an output file were passed
		if len (inputFiles) > 1 and not options.outputFile[0] == ".":
			# More than an input file was passed, but a single non-".xxx"
			# output file was given
			print >> sys.stderr, "When specifying more than an input file, you must use .xxx as output file"
		else:
			# Init CM
			cm = CodecManager ()
			for inputFile in inputFiles:
				outFile = makeOutputFilename (inputFile, options.outputFile)
				transcode (cm, inputFile, outFile, options.output_quality, options.overwrite, progressCallback = ProgressMeter ())
	else:
		print >> sys.stderr, "Please specify at least an input and an output file!"

if __name__ == '__main__':
	main ()
