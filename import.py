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

# import chrome files into the l10n repository
def chrome2l10n(chrome_dir, l10n_dir, index_file):
	print "importing " + chrome_dir + " to " + l10n_dir + ", following " + index_file
	infile = open(index_file, "r")
	for line in infile:
		# ignore line if chrome and/or l10n is not defined
		if line.find(chrome_sep)>0 and line.find(l10n_sep)>0:
			# get chrome and l10n paths
			tmp    = line.partition(l10n_sep)
			l10n   = l10n_dir + tmp[2].strip()
			tmp    = tmp[0].partition(chrome_sep)
			chrome = chrome_dir + tmp[2].strip()
			# copy chrome file to l10n directory
			xcopy(chrome, l10n)

# main
if len(sys.argv) < 3:
	# not enough arguments, display usage
	print "usage:"
	print "    ./import.py chrome_dir l10n_dir [index]"
	print 
	print "arguments:"
	print "    chrome_dir : chrome-path locale directory to import"
	print "    l10n_dir   : destination l10n directory"
	print "    [index]    : optional index file (index.mn by default)"
	print 
	print "example:"
	print "    ./import.py chrome/fr-FR/ l10n/fr/"
	print 
else:
	# check arguments
	chrome_dir = sys.argv[1]
	l10n_dir   = sys.argv[2]
	if len(sys.argv) > 3:
		index_file = sys.argv[3]
	else:
		index_file = "index.mn"
	# go, go, go!
	chrome2l10n(chrome_dir, l10n_dir, index_file)

