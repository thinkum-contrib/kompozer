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

index_file = "index.mn"
import_dir = "l10n.CVS/"
l10n_sep   = "(l10n)"
debug      = 1

def shell(cmd):
	if debug:
		print(cmd)
	else:
		os.system(cmd)

# import chrome files to the l10n repository
def l10nCopy(source_dir, dest_dir):

	infile = open(index_file, "r")
	for line in infile:

		# ignore line if l10n is not defined
		if line.find(l10n_sep)>0:

			# get l10n paths
			tmp       = line.partition(l10n_sep)
			l10n_file = tmp[2].strip()
			l10n_dir  = l10n_file.rpartition("/")[0]
			source    = source_dir + l10n_file
			dest      = dest_dir   + l10n_file
			dir       = dest_dir   + l10n_dir

			# copy file to l10n directory
			if os.path.exists(source):
				shell("mkdir -p " + dir)
				shell("cp -p " + source + " " + dest)
			else:
				print("### could not find " + source)

# main: copy all locales from "l10n.CVS" to "l10n"
dirList = os.listdir(import_dir)
for dir in dirList:
	if dir != "CVS":
		l10nCopy(import_dir + dir, "l10n/" + dir)

