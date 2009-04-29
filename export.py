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

# export chrome files from the l10n repository
def l10n2chrome(locale):

	infile = open(index_file, "r")
	for line in infile:

		# ignore line if chrome and/or l10n is not defined
		if line.find(chrome_sep)>0 and line.find(l10n_sep)>0:

			# get chrome and l10n paths
			tmp    = line.partition(l10n_sep)
			l10n   = "l10n/" + locale + tmp[2].strip()
			tmp    = tmp[0].partition(chrome_sep)[2].rpartition("/")
			chrome = "chrome/" + locale + tmp[0].strip()

			# copy l10n file to chrome directory
			os.system("mkdir -p " + chrome)
			os.system("cp -p " + l10n + " " + chrome)

l10n2chrome("fr")
