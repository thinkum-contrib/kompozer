#!/usr/bin/python
# purpose     : l10n utility script for KompoZer 0.8
# developer   : Fabien Cazenave <kaze@kompozer.net>
# last update : 2009-05-02

###############################################################################
#                                                                             #
#                                WTFPL v2                                     #
#                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE                  #
#                        Version 2, December 2004                             #
#                                                                             #
#     Copyright (C) 2004 Sam Hocevar                                          #
#                        14 rue de Plaisance, 75014 Paris, France             #
#     Everyone is permitted to copy and distribute verbatim or modified       #
#     copies of this license document, and changing it is allowed as long     #
#     as the name is changed.                                                 #
#                                                                             #
#                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE                  #
#      TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION        #
#                                                                             #
#      0. You just DO WHAT THE FUCK YOU WANT TO.                              #
#                                                                             #
###############################################################################

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the WTFPL, version 2.

import os
import sys

# preferences: adapt these lines to your config
L10N_ROOT     = "l10n/"
CHROME_ROOT   = "../chrome/"
IMPORT_ROOT   = "../l10n.CVS/"
INDEX_FILE    = "index.mn"

# these files should be in the l10n directory
BRAND_FILE    = L10N_ROOT + "brand.dtd"
VERSION_FILE  = L10N_ROOT + "version.txt"
INSTALL_FILE  = L10N_ROOT + "install.rdf"
MANIFEST_FILE = L10N_ROOT + "chrome.manifest"
PREFS_FILE    = L10N_ROOT + "prefs.js"

# don't touch this unless you know what you're doing
L10N_SEP      = "(l10n)"
CHROME_SEP    = "(chrome)"
DEBUG         = 0


###############################################################################
#                                                                             #
#     Helper functions                                                        #
#                                                                             #
###############################################################################

# shell access, check the value of "DEBUG"
def shell(cmd):
	if DEBUG:
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


###############################################################################
#                                                                             #
#     l10n converters                                                         #
#                                                                             #
###############################################################################

# copy all locales from "l10n.CVS" to "l10n", check value of "IMPORT_ROOT" above
def l10nCopyAll():
	dirList = os.listdir(IMPORT_ROOT)
	for dir in dirList:
		if dir != "CVS":
			l10nCopy(IMPORT_ROOT + dir, "l10n/" + dir)


# import relevant files in the Mozilla CVS trunk (= 1.8.1) to the KompoZer l10n repository
# cvs -d :pserver:anonymous@cvs-mirror.mozilla.org/l10n co l10n
def l10nCopy(sourceDir, destDir):
	print "copying " + sourceDir + " to " + destDir + ", following " + INDEX_FILE

	infile = open(INDEX_FILE, "r")
	for line in infile:

		# ignore line if l10n is not defined
		if line.find(L10N_SEP)>0:

			# get l10n paths
			tmp       = line.partition(L10N_SEP)
			l10n_file = tmp[2].strip()
			source    = sourceDir + l10n_file
			dest      = destDir   + l10n_file

			# copy file to l10n directory
			xcopy(source, dest)


# import chrome files into the l10n repository
def chrome2l10n(chromeDir, l10nDir):
	print "importing " + chromeDir + " to " + l10nDir + ", following " + INDEX_FILE

	infile = open(INDEX_FILE, "r")
	for line in infile:

		# ignore line if chrome and/or l10n is not defined
		if line.find(CHROME_SEP)>0 and line.find(L10N_SEP)>0:

			# get chrome and l10n paths
			tmp    = line.partition(L10N_SEP)
			l10n   = l10nDir + tmp[2].strip()
			tmp    = tmp[0].partition(CHROME_SEP)
			chrome = chromeDir + tmp[2].strip()

			# copy chrome file to l10n directory
			xcopy(chrome, l10n)


# export chrome files from the l10n repository
def l10n2chrome(l10nDir, chromeDir):
	print "exporting " + l10nDir + " to " + chromeDir + ", following " + INDEX_FILE

	infile = open(INDEX_FILE, "r")
	for line in infile:

		# ignore line if chrome and/or l10n is not defined
		if line.find(CHROME_SEP)>0 and line.find(L10N_SEP)>0:

			# get chrome and l10n paths
			tmp    = line.partition(L10N_SEP)
			l10n   = l10nDir + tmp[2].strip()
			tmp    = tmp[0].partition(CHROME_SEP)
			chrome = chromeDir + tmp[2].strip()

			# copy l10n file to chrome directory
			xcopy(l10n, chrome)

	# this file has to be added separately (not to be translated)
	xcopy(BRAND_FILE, chromeDir + "/global/brand.dtd")


# create XPI langpack from a chrome-path directory
def chrome2xpi(locale):
	# warning: won't work on Windows unless you're in a Cygwin shell
	xpiFile = "kompozer-" + locale + ".xpi"
	print "making " + xpiFile

	# remove xpiFile if existing
	if os.path.exists(CHROME_ROOT + xpiFile):
		shell("rm " + CHROME_ROOT + xpiFile)

	# create a temp directory
	tmpDir = "~" + locale + ".tmp/"
	if os.path.exists(CHROME_ROOT + tmpDir):
		shell("rm -rf " + CHROME_ROOT + tmpDir)
	tmpChrome = tmpDir + "chrome/"
	tmpPrefs  = tmpDir + "defaults/preferences/"
	shell("mkdir -p " + CHROME_ROOT + tmpChrome)
	shell("mkdir -p " + CHROME_ROOT + tmpPrefs)

	# replace @AB_CD@ with 'locale' in chrome.manifest, install.rdf and prefs.js
	sed = "sed s/@AB_CD@/" + locale + "/g "
	shell(sed + MANIFEST_FILE + " > " + CHROME_ROOT + tmpDir   + "chrome.manifest")
	shell(sed + INSTALL_FILE  + " > " + CHROME_ROOT + tmpDir   + "install.rdf")
	shell(sed + PREFS_FILE    + " > " + CHROME_ROOT + tmpPrefs + "prefs.js")

	# make a JAR
	os.chdir(CHROME_ROOT)
	tmpJar = locale + ".jar"
	if os.path.exists(tmpJar):
		shell("rm " + tmpJar)
	shell("zip -qr " + tmpJar + " " + locale)
	shell("mv " + tmpJar + " " + tmpChrome)

	# make an XPI
	os.chdir(tmpDir)
	shell("zip -qr " + xpiFile + " *")
	shell("mv " + xpiFile + " ..")

	# remove temp files
	os.chdir("..")
	shell("rm -rf " + tmpDir)


###############################################################################
#                                                                             #
#     Command-line handling                                                   #
#                                                                             #
###############################################################################

# script usage information
def usage():
	print 
	print "usage:"
	print "    ./convert-locales.py <command> locale [index]"
	print 
	print "command:"
	print "    copy : copy all files required by KompoZer from a Mozilla-CVS l10n directory"
	print "    push : copy files from the chrome-path directory to the l10n directory"
	print "    pull : copy files from the l10n directory to the chrome-path directory"
	print "    make : create an XPI langpack from the chrome-path directory"
	print 
	print "locale:"
	print "    locale identifier, e.g. 'en-US' or 'fr'"
	print 
	print "index:"
	print "    optional index file for the [copy|push|pull] commands"
	print "    default is '" + INDEX_FILE + "'"
	print 
	print "current settings:"
	print "    l10n directory        : " + L10N_ROOT
	print "    chrome-path directory : " + CHROME_ROOT
	print "    Mozilla-CVS directory : " + IMPORT_ROOT
	print "    (please edit this script if you want to change these settings)"
	print 
	print "examples:"
	print "    ./convert-locales.py push en-US"
	print "    ./convert-locales.py pull fr"
	print "    ./convert-locales.py make fr"
	print 

# main: parse command-line arguments
if len(sys.argv) < 3:
	usage()
else:
	command    = sys.argv[1]
	locale     = sys.argv[2]
	chrome_dir = CHROME_ROOT + locale
	l10n_dir   = L10N_ROOT   + locale
	if len(sys.argv) > 3:
		INDEX_FILE = sys.argv[3]
	# go, go, go!
	if (command == "copy"):
		l10nCopy(l10n_import + sys.argv[2], l10n_dir)
	elif (command == "push"):
		chrome2l10n(chrome_dir, l10n_dir)
	elif (command == "pull"):
		l10n2chrome(l10n_dir, chrome_dir)
	elif (command == "make"):
		chrome2xpi(locale)
	else:
		usage()

