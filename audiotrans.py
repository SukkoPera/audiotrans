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
from AudioTrans.ByteSwapper import ByteSwapper

PROGRAM_VERSION = "20151223"
BUFSIZE = 1024 * 8

def progress (stepNo):
	sequence = ["|", "/", "-", "\\"]
	print >> sys.stderr, "\r%s" % sequence[stepNo % len (sequence)],
	sys.stderr.flush ()


def transcode (codecsMgr, infile, outfile, quality, overwrite = False, transferTag = True):
	print "%s -> %s" % (infile, outfile)
	if os.path.isfile (outfile) and not overwrite:
		print "- Skipping because \"%s\" already exists" % outfile
	else:
		step = 0
		dec = codecsMgr.getDecoder (infile)
		enc = codecsMgr.getEncoder (outfile, quality)
		filt = ByteSwapper (dec, enc)
		decproc = enc.getProcess ()
		encproc = enc.getProcess ()
		buf = filt.read (BUFSIZE)
		while len (buf) > 0:
			progress (step)
			step += 1
			encproc.write (buf)
			#progress (step)
			#step += 1
			buf = filt.read (BUFSIZE)
		filt.close ()
		encproc.close ()
		decproc.close ()

		# Transfer tag
		if transferTag:
			tag = dec.getTag ()
			#~ print tag
			enc.setTag (tag)

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
			print "When specifying more than an input file, you must use .xxx as output file"
		else:
			# Init CM
			cm = CodecManager ()
			for inputFile in inputFiles:
				outFile = makeOutputFilename (inputFile, options.outputFile)
				transcode (cm, inputFile, outFile, options.output_quality, options.overwrite)
	else:
		print "Please specify at least an input and an output file!"

if __name__ == '__main__':
	main ()
