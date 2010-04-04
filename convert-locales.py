#!/usr/bin/env python
# author      : Fabien Cazenave <kaze@kompozer.net>
# purpose     : l10n utility script for KompoZer 0.8
# requires    : bash + Python 2.5
#               successfully tested on GNU/Linux
#               not tested on Windows or MacOSX yet
# last update : 2009-03-01

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

VERSION = "0.8b3"


###############################################################################
#                                                                             #
#  This script converts data frome chrome/ to l10n/ and build/                #
#   - basically, it builds language packs :-)                                 #
#                                                                             #
###############################################################################
#                                                                             #
#  build/                                                                     #
#    = output directory for the language packs (JAR and XPI files)            #
#                                                                             #
#  chrome/                                                                    #
#    = main directory, used to:                                               #
#       * import/export data from/to l10n/      (l10n2chrome, chrome2l10n)    #
#       * generate JAR and XPI files in build/   (chrome2jar, chrome2xpi)     #
#    chrome-path file structure:                                              #
#      all files in chrome/ are stored as they are in a language pack         #
#                                                                             #
#  l10n/                                                                      #
#    = clone of the mercurial repository                                      #
#    the file structure conforms to the official Mozilla l10n repositories    #
#    but it can't be used 'as is' to generate language packs                  #
#                                                                             #
###############################################################################

# preferences: adapt these lines to your config
L10N_ROOT     = "l10n/"
IMPORT_ROOT   = "l10n.CVS/"
CHROME_ROOT   = "chrome/"
INDEX_FILE    = "index.mn"

# these files are expected to be in the l10n directory
BRAND_FILE    = L10N_ROOT + "brand.dtd"
INSTALL_FILE  = L10N_ROOT + "install.rdf"
MANIFEST_FILE = L10N_ROOT + "chrome.manifest"
PREFS_FILE    = L10N_ROOT + "prefs.js"

# output directories
BUILD_ROOT    = "build/"
BUILD_JAR     = "build/jar/"
BUILD_XPI     = "build/xpi/"

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
#     L10n utilities                                                          #
#                                                                             #
###############################################################################

# import relevant files in the Mozilla CVS trunk (= 1.8.1) to the KompoZer l10n repository
# cvs -d :pserver:anonymous@cvs-mirror.mozilla.org/l10n co l10n
def l10nCopy(sourceDir, destDir, indexFile):
  print "copying " + sourceDir + " to " + destDir + " following " + indexFile

  infile = open(indexFile, "r")
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

# pull chrome files from the l10n repository
def l10n2chrome(l10nDir, chromeDir):
  print "exporting " + l10nDir + " to " + chromeDir + " following " + INDEX_FILE

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

# push chrome files into the l10n repository
def chrome2l10n(chromeDir, l10nDir, indexFile):
  print "importing " + chromeDir + " to " + l10nDir + " following " + indexFile

  infile = open(indexFile, "r")
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

# create a JAR archive from a chrome-path directory
def chrome2jar(locale):
  cwd = os.getcwd()
  if not os.path.exists(CHROME_ROOT + locale):
    l10n2chrome(L10N_ROOT + locale, CHROME_ROOT + locale)

  # create a temp dir in BUILD_JAR
  tmpDir = BUILD_JAR + "locale/"
  if os.path.exists(tmpDir):
    shell("rm -rf " + tmpDir)
  shell("mkdir -p " + tmpDir)
  shell("cp -R " + CHROME_ROOT + locale + " " + tmpDir) # cloneDirectory?

  # make [locale].jar in BUILD_JAR
  os.chdir(BUILD_JAR)
  jarFile = locale + ".jar"
  if os.path.exists(jarFile):
    shell("rm " + jarFile)
  shell("zip -qr -0 " + jarFile + " locale/")
  os.chdir(cwd)

  # remove temp dir, done
  shell("rm -rf " + tmpDir)
  return BUILD_JAR + jarFile

# create an XPI langpack from a chrome-path directory
def chrome2xpi(locale):
  cwd = os.getcwd()
  xpiFile = "kompozer-" + VERSION + "." + locale + ".xpi"
  if os.path.exists(xpiFile):
    shell("rm " + xpiFile)
  print "making " + BUILD_XPI + xpiFile

  # create a temp dir
  tmpDir = BUILD_XPI + "~" + locale + ".tmp/"
  if os.path.exists(tmpDir):
    shell("rm -rf " + tmpDir)
  tmpChrome = tmpDir + "chrome/"
  tmpPrefs  = tmpDir + "defaults/preferences/"
  shell("mkdir -p " + tmpChrome)
  shell("mkdir -p " + tmpPrefs)

  # replace @AB_CD@ with 'locale' in chrome.manifest, install.rdf and prefs.js
  sed = "sed s/@AB_CD@/" + locale + "/g "
  shell(sed + MANIFEST_FILE + " > " + tmpDir   + "chrome.manifest")
  shell(sed + INSTALL_FILE  + " > " + tmpDir   + "install.rdf")
  shell(sed + PREFS_FILE    + " > " + tmpPrefs + "prefs.js")

  # make kompozer-[VERSION].[locale].xpi in BUILD_XPI
  jarFile = chrome2jar(locale) # add [locale].jar to the 'chrome' subdir
  shell("cp " + jarFile + " " + tmpChrome)
  os.chdir(tmpDir)
  shell("zip -qr " + cwd + "/" + BUILD_XPI + xpiFile + " *")
  os.chdir(cwd)

  # remove temp files, done
  shell("rm -rf " + tmpDir)
  return BUILD_XPI + xpiFile


###############################################################################
#                                                                             #
#     Command-line handling                                                   #
#                                                                             #
###############################################################################

# script usage information
def usage(full):
  print "usage:"
  print "    ./convert-locales.py <command> locale [index] [source]"
  print 
  if (full):
    print "command:"
    print "    copy : copy all files required by KompoZer from a Mozilla-CVS l10n directory"
    print "    push : copy files from the chrome-path directory to the l10n directory"
    print "    pull : copy files from the l10n directory to the chrome-path directory"
    print "    make : create an XPI langpack from the chrome-path directory"
    print "    help : display this message"
    print 
    print "locale:"
    print "    locale identifier, e.g. 'en-US' or 'fr'"
    print "    use 'all' to process all available locales"
    print 
    print "index:"
    print "    optional index file for the [copy|push] commands"
    print "    default is '" + INDEX_FILE + "'"
    print 
    print "source:"
    print "    optional source directory for the [copy|push] commands"
    print "    will be used instead of the locale in the chrome-path directory"
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
  else:
    print "To get the full help, please use:"
    print "    ./convert-locales.py help"
    print 
  print "You probably want to run:"
  print "    ./convert-locales.py make all"
  print "to generate all available XPI langpacks in the " + CHROME_ROOT + " directory."
  print 

# main: parse command-line arguments
def main():
  if len(sys.argv) < 2:
    usage(0)
  elif len(sys.argv) == 2:
    usage(sys.argv[1].endswith("help"))

  else:
    # get command and locale arguments
    command = sys.argv[1]
    locale  = sys.argv[2]

    # 'push' and 'copy' put files into the 'l10n' directory
    # and may get two additional parameters: index and source
    if command == "push" or command == "copy":
      if locale == "all":
        print "'all' is not allowed with '" + command + "'"
        sys.exit()
      # default parameters
      index_file = INDEX_FILE
      import_dir = IMPORT_ROOT + locale
      chrome_dir = CHROME_ROOT + locale
      l10n_dir   = L10N_ROOT   + locale
      # specific parameters
      if len(sys.argv) > 3:
        index_file = sys.argv[3]
      if len(sys.argv) > 4:
        import_dir = sys.argv[4]
        chrome_dir = sys.argv[4]
      # process command on the requested locale
      if command == "copy" and os.path.isdir(import_dir):
        l10nCopy(import_dir, l10n_dir, index_file)
      elif command == "push" and os.path.isdir(chrome_dir):
        chrome2l10n(chrome_dir, l10n_dir, index_file)
      sys.exit()

    # 'pull' and 'make' read files from the 'l10n' directory
    # and may get 'all' as locale identifier
    elif command == "pull" or command == "make":
      if locale == "all":
        localeList = os.listdir(L10N_ROOT)
      else:
        localeList = []
        localeList.append(locale)
      # process command on each locale (ignore 'CVS' and hidden directories)
      for locale in localeList:
        if os.path.isdir(L10N_ROOT + locale) and locale != "CVS" and not locale.startswith("."):
          if (command == "pull"):
            l10n2chrome(L10N_ROOT + locale, CHROME_ROOT + locale)
          elif (command == "make"):
            chrome2xpi(locale)
      sys.exit()
    
    else:
      print "Error: invalid command '" + command + "'"
      print
      usage(1)
      sys.exit()

if __name__ == "__main__":
  main()

