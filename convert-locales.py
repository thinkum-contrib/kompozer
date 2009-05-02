#!/usr/bin/python
# l10n utility script for KompoZer 0.8

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the WTFPL, version 2.

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

import os
import sys

# adapt these lines to your config
l10n_root   = "l10n/"
chrome_root = "../chrome/"
import_dir  = "../l10n.CVS/"
index_file  = "index.mn"
brand_file  = "l10n/brand.dtd"
tmp_dir     = "../tmp"

# don't touch this unless you know what you're doing
l10n_sep    = "(l10n)"
chrome_sep  = "(chrome)"
debug       = 0

# shell access, check the value of "debug"
def shell(cmd):
	if debug:
		print(cmd)
	else:
		os.system(cmd)

# copy source to dest and create directory if needed
def xcopy(source, dest):
  # warning: won't work on Windows unless you're in a Cygwin shell
	if os.path.exists(source):
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

# copy all locales from "l10n.CVS" to "l10n"
# check value of "import_dir" above
def l10nCopyAll():
  dirList = os.listdir(import_dir)
  for dir in dirList:
    if dir != "CVS":
      l10nCopy(import_dir + dir, "l10n/" + dir)

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

# export chrome files from the l10n repository
def l10n2chrome(l10n_dir, chrome_dir):
	print "exporting " + l10n_dir + " to " + chrome_dir + ", following " + index_file
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
	# this file has to be added separately (not to be translated)
	xcopy(brand_file, chrome_dir + "/global/brand.dtd")

# create XPI langpack from a chrome-path directory
def chrome2xpi(locale):
  # warning: won't work on Windows unless you're in a Cygwin shell
  sed = "sed s/@AB_CD@/" + locale + "/g " + l10n_root
  # replace @AB_CD@ with 'locale' in *.manifest and install.rdf
  manifest = chrome_root + locale + ".manifest"
  install  = chrome_root + "install.rdf"
  shell(sed + "locale.manifest > " + manifest)
  shell(sed + "install.rdf > " + install)
  # make a JAR
  os.chdir(chrome_root)
  if os.path.exists(locale + ".jar"):
    shell("rm " + locale + ".jar")
  shell("zip -qr " + locale + ".jar " + locale)
  # make an XPI
  shell("zip -qr " + locale + ".xpi " + locale + ".jar " + locale + ".manifest install.rdf")
  # remove temp files
  shell("rm " + locale + ".jar")
  shell("rm " + manifest)
  shell("rm " + install)

# script usage information
def usage():
	print "usage:"
	print "    ./convert-locales.py <command> locale [index]"
	print 
	print "command:"
	print "    copy   : copy all files required by KompoZer from an Mozilla-CVS l10n directory"
	print "    import : import files from the chrome-path directory into the l10n directory"
	print "    export : export files from the l10n directory to the chrome-path directory"
	print "    make   : create an XPI langpack from the chrome-path directory"
	print 
	print "locale:"
	print "    locale identifier, e.g. 'en-US' or 'fr'"
	print 
	print "index:"
	print "    optional index file for the 'import' command - default is 'index.mn'"
	print 
	print "options:"
	print "    please edit this script to set specific options"
	print 
	print "examples:"
	print "    ./convert-locales.py import en-US"
	print "    ./convert-locales.py export fr"
	print "    ./convert-locales.py make fr"
	print 

# main: parse command-line arguments
if len(sys.argv) < 3:
	usage()
else:
	command    = sys.argv[1]
	locale     = sys.argv[2]
	chrome_dir = chrome_root + locale
	l10n_dir   = l10n_root   + locale
	if len(sys.argv) > 3:
		index_file = sys.argv[3]
	# go, go, go!
	if (command == "copy"):
		l10nCopy(l10n_import + sys.argv[2], l10n_dir)
	elif (command == "import"):
		chrome2l10n(chrome_dir, l10n_dir)
	elif (command == "export"):
		l10n2chrome(l10n_dir, chrome_dir)
	elif (command == "make"):
		chrome2xpi(locale)
	else:
		usage()

