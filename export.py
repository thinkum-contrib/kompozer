#!/usr/bin/python

#                            WTFPL v2
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar
#  14 rue de Plaisance, 75014 Paris, France
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO. 
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the WTFPL, version 2.
# See http://sam.zoy.org/wtfpl/COPYING for more details.

import os
import sys

index_file = "index.mn"
chrome_sep = "(chrome)"
l10n_sep   = "(l10n)"
debug      = 0

# shell access, check the value of "debug"
def shell(cmd):
	if debug:
		print(cmd)
	else:
		os.system(cmd)

# copy source to dest and create directory if needed
def xcopy(source, dest):
	if os.path.exists(source):
		# warning: not working on Windows
		shell("mkdir -p " + dest.rpartition("/")[0])
		shell("cp -p " + source + " " + dest)
	else:
		print("### could not find " + source)

# export chrome files from the l10n repository
def l10n2chrome(l10n_dir, chrome_dir):
	infile = open(index_file, "r")
	for line in infile:
		# ignore line if chrome and/or l10n is not defined
		if line.find(chrome_sep)>0 and line.find(l10n_sep)>0:
			# get chrome and l10n paths
			tmp    = line.partition(l10n_sep)
			l10n   = l10n_dir + tmp[2].strip()
			tmp    = tmp[0].partition(chrome_sep)
			chrome = chrome_dir + tmp[2].strip()
			# copy l10n file to chrome directory
			xcopy(l10n, chrome)

#l10n2chrome("fr")
if len(sys.argv) < 3:
	# not enough arguments, display usage
	print "usage:"
	print "    ./export.py l10n_dir chrome_dir"
	print 
	print "arguments:"
	print "    l10n_dir   : source l10n directory"
	print "    chrome_dir : chrome-path locale directory to create/update"
	print 
	print "example:"
	print "    ./export.py l10n/fr/ chrome/fr-FR/"
	print 
else:
	# check arguments
	l10n_dir   = sys.argv[1]
	chrome_dir = sys.argv[2]
	# go, go, go!
	l10n2chrome(l10n_dir, chrome_dir)
	# this file has to be added separately (not to be translated)
	xcopy("l10n/brand.dtd", chrome_dir + "global/brand.dtd")

