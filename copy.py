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

# import relevant files in the Mozilla CVS trunk (= 1.8.1) to the KompoZer l10n repository
# cvs -d :pserver:anonymous@cvs-mirror.mozilla.org/l10n co l10n
def l10nCopy(source_dir, dest_dir):
	infile = open(index_file, "r")
	for line in infile:
		# ignore line if l10n is not defined
		if line.find(l10n_sep)>0:
			# get l10n paths
			tmp       = line.partition(l10n_sep)
			l10n_file = tmp[2].strip()
			source    = source_dir + l10n_file
			dest      = dest_dir   + l10n_file
			# copy file to l10n directory
			xcopy(source, dest)

# main: copy all locales from "l10n.CVS" to "l10n"
# check value of "import_dir" above
dirList = os.listdir(import_dir)
for dir in dirList:
	if dir != "CVS":
		l10nCopy(import_dir + dir, "l10n/" + dir)

