#!/usr/bin/python
# author      : Fabien Cazenave <kaze@kompozer.net>
# purpose     : l10n utility script for KompoZer 0.8
# last update : 2010-02-24

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
#LOCALES = ["ca", "da", "de", "en-US", "es-ES", "fi", "fr", "hu", "hsb", "it", "ja", "pt-PT", "ru", "zh-CN", "zh-TW"]
LOCALES = ["en-US", "fr", "ru", "zh-TW"] # debug

###############################################################################
#                                                                             #
# INPUT: en-US raw binaries                                                   #
# -------------------------                                                   #
#                                                                             #
#   LINUX                MacOSX                     WIN32                     #
#                          KompoZer.app/                                      #
#                            Contents/                                        #
#     kompozer/                MacOS/                 KompoZer/               #
#       chrome/                  chrome/                chrome/               #
#         en-US.jar                en-US.jar              en-US.jar           #
#         en-US.manifest           en-US.manifest         en-US.manifest      #
#       defaults/                defaults/              defaults/             #
#         pref/                    pref/                  pref/               #
#           all.js                   all.js                 all.js            #
#           editor.js                editor.js              editor.js         #
#         profile/                 profile/               profile/            #
#       dictionaries/            dictionaries/          dictionaries/         #
#         en-US.aff                en-US.aff              en-US.aff           #
#         en-US.dic                en-US.dic              en-US.dic           #
#                              Resources/                                     #
#                                en.lproj                                     #
#                                                                             #
###############################################################################
#                                                                             #
# OUTPUT: localized binaries                                                  #
# --------------------------                                                  #
#                                                                             #
# build/                                                                      #
#   test/                [version]/                                           #
#     linux-i686/          linux-i686/                                        #
#       %ab_cd%              kompozer-%version%.%ab_cd%-gcc4.2-i686.tar.gz    #
#         kompozer/        macosx/                                            #
#     macosx/                kompozer-%version%.%ab_cd%-macosx-universal.dmg  #
#       %ab_cd%            win32/                                             #
#         kompozer.app/      exe/                                             #
#     win32/                   kompozer-%version%.%ab_cd%-win32.exe           #
#       %ab_cd%              zip/                                             #
#         kompozer/            kompozer-%version%.%ab_cd%-win32.zip           #
#                                                                             #
###############################################################################

# preferences: adapt these lines to your config
CHROME_ROOT     = "chrome/"
MYSPELL_ROOT    = "myspell/"
BUILD_ROOT      = "build/"
BUILD_TEST      = "build/test/"


###############################################################################
#                                                                             #
#     Shell helpers                                                           #
#                                                                             #
###############################################################################

DEBUG = 0

# Shell access
# check the value of "DEBUG" above
def shell(cmd):
  if DEBUG:
    print(cmd)
  else:
    os.system(cmd)

# Replace all found occurrences in 'filePath'
# ('sed -i' doesn't work on MacOSX as it does on GNU/Linux)
def replaceInFile(findStr, replaceStr, filePath):
  sed = "sed 's/" + findStr + "/" + replaceStr + "/g' "
  shell(sed + filePath + " > " + filePath + "~")
  shell("mv " + filePath + "~ " + filePath)

# Clone the 'srcPath' directory as a child of 'destPath'
#   and return the new directory's path
# ('cp -r' doesn't work on MacOSX as it does on GNU/Linux)
def cloneDirectory(srcPath, destPath):
  if srcPath[-1:] == "/": # remove trailing slash if any
    srcPath = srcPath[0:-1]
  baseName = os.path.basename(srcPath)

  # get an empty destPath/baseName directory
  if destPath[-1:] == "/": # remove trailing slash if any
    destPath = dir[0:-1]
  destDir = destPath + "/" + baseName
  if os.path.exists(destDir):
    shell("rm -rf " + destDir + "/*")
  else:
    shell("mkdir -p " + destDir)

  # copy 'srcPath' content to 'destPath/baseName'
  shell("cp -R " + srcPath + "/* " + destDir)
  return destDir + "/"


###############################################################################
#                                                                             #
#     L10n utilities                                                          #
#                                                                             #
###############################################################################

# make [locale].jar
def makeJAR(locale):
  jarDir = os.getcwd() + "/" + CHROME_ROOT
  os.chdir(jarDir)
  jar = locale + ".jar"
  if os.path.exists(jar):
    #shell("rm " + jar)
    return jarDir + jar
  if os.path.exists("locale"):
    shell("rm -rf locale")
  shell("mkdir locale")
  shell("cp -R " + locale + " locale/")
  shell("zip -qr -0 " + jar + " locale")
  shell("rm -rf locale")
  return jarDir + jar

# create localized binary
def makeBinary(srcDir, platform, locale):
  cwd = os.getcwd() + "/"

  # set base directories
  destDir = cwd + BUILD_TEST
  if (platform == "linux"):
    destDir += "linux-i686/" + locale
    binDir = destDir + "/kompozer/"
  elif (platform == "mac"):
    destDir += "macosx/" + locale
    binDir = destDir + "/KompoZer.app/Contents/MacOS/"
  elif (platform == "win"):
    destDir += "win32/" + locale
    binDir = destDir + "/KompoZer/"
  else:
    print("unsupported platform")
    return
  chromeDir  = binDir + "chrome/"
  prefsDir   = binDir + "defaults/pref/"
  profileDir = binDir + "defaults/profile/"
  dictDir    = binDir + "dictionaries/"

  # create a directory for the new localized build
  cloneDirectory(srcDir, destDir)

  # remove unused files
  shell("rm " + chromeDir + "chromelist.txt")
  shell("rm " + profileDir + "*.js")
  shell("rm -rf " + profileDir + "US")

  # if we're packing the en-US binary, we're done
  if (locale == "en-US"):
    return destDir

  # replace en-US.* by [locale].*
  tmpJar = makeJAR(locale)
  os.chdir(chromeDir)
  sed = "sed s/en-US/" + locale + "/g "
  shell(sed + "en-US.manifest > " + locale  + ".manifest")
  os.chdir(cwd)
  shell("rm " + chromeDir + "en-US.*")
  shell("cp " + tmpJar + " " + chromeDir)

  # MacOSX: rename en.lproj as [locale].lproj
  if (platform == "mac"):
    os.chdir(destDir + "/KompoZer.app/Contents/Resources/")
    if (locale == "ca"):
      shell("mv en.lproj ca-AD.lproj")
    elif (locale == "hu"):
      shell("mv en.lproj hu-HU.lproj")
    else:
      shell("mv en.lproj " + locale + ".lproj")

  # change locale in all.js
  os.chdir(prefsDir)
  replaceInFile("en-US", locale, "all.js")

  # some locales require specific char encodings
  acceptCharsets = "iso-8859-1,\*,utf-8"
  customCharset  = "ISO-8859-1"
  if (locale == "ja"):
    replaceInFile(acceptCharsets, "Shift_JIS,\*,utf-8",    "all.js")
    replaceInFile(customCharset,  "Shift_JIS",             "editor.js")
  elif (locale == "zh-CN" or locale == "zh-TW" or locale == "hsb"):
    replaceInFile(acceptCharsets, "utf-8,\*,iso-8859-1",   "all.js")
    replaceInFile(customCharset,  "UTF8",                  "editor.js")
  elif (locale == "hu" or locale == "pl"):
    replaceInFile(acceptCharsets, "iso-8859-2,\*,utf-8",   "all.js")
    replaceInFile(customCharset,  "ISO-8859-2",            "editor.js")
  elif (locale == "ru"):
    replaceInFile(acceptCharsets, "Windows-1251,\*,utf-8", "all.js")
    replaceInFile(customCharset,  "Windows-1251",          "editor.js")

  # include tri-licensed mySpell dictionary, if any
  os.chdir(cwd)
  shell("rm " + dictDir + "*")
  myspellDir = MYSPELL_ROOT + locale
  if os.path.exists(myspellDir):
    shell("cp " + myspellDir + "/* " + dictDir)

  return destDir

# pack localized binary
def makePackage(srcDir, platform, locale):
  cwd = os.getcwd() + "/"
  baseDir = cwd + BUILD_ROOT + VERSION
  baseFile = "kompozer-" + VERSION + "." + locale
  os.chdir(srcDir)

  # Linux: tar.gz archive
  if (platform == "linux"):
    baseDir += "/linux-i686/"
    baseFile += "-gcc4.2-i686.tar.gz"
    shell("mkdir -p " + baseDir)
    shell("tar -chzf " + baseDir + baseFile + " kompozer")

  # MacOSX: dmg image
  elif (platform == "mac"):
    baseDir += "/macosx/"
    baseFile += "-macosx-universal.dmg"
    shell("mkdir -p " + baseDir)
    srcfolder = ' -srcfolder "' + srcDir + '"'
    volname = ' -volname "KompoZer ' + locale + '" '
    options = ' -format UDZO -imagekey zlib-level=9 '
    dmgFile = baseDir + baseFile
    if os.path.exists(dmgFile):
      shell("rm " + dmgFile)
    shell("hdiutil create -srcfolder ." + volname + dmgFile + options)

  # Win32: zip (+ installer)
  elif (platform == "win"):
    baseDir += "/win32/"
    zipFile = baseDir + "zip/" + baseFile + "-win32.zip"
    exeFile = baseDir + "exe/" + baseFile + "-win32.exe"
    shell("mkdir -p " + baseDir + "zip")
    shell("mkdir -p " + baseDir + "exe")
    # TODO

  # mismatch
  else:
    print("unsupported platform")
    return

  # done
  os.chdir(cwd)
  return


###############################################################################
#                                                                             #
#     Command-line handling                                                   #
#                                                                             #
###############################################################################

# main: parse command-line arguments
def main():
  if len(sys.argv) < 2: # not enough arguments
    print("usage: ./release.py [path/to/kompozer/directory]")
    return

  # get binary directory and target platform
  srcPath = sys.argv[1]
  if srcPath[-1:] == "/":
    srcPath = srcPath[0:-1]
  if os.path.basename(srcPath) == "KompoZer.app":
    platform = "mac"
  elif os.path.exists(srcPath + "/kompozer.exe"):
    platform = "win"
  elif os.path.exists(srcPath + "/kompozer-bin"):
    platform = "linux"
  else:
    print("not a kompozer binary.")
    return

  # get the list of the locales to build
  if (len(sys.argv) > 2):
    # build specified locales (TODO)
    locale = sys.argv[2]
  else:
    # build all locales
    locales = LOCALES
    locale = "fr"

  # build
  print
  print("building kompozer-" + VERSION + "." + locale + " (" + platform + ")...")
  srcDir = makeBinary(srcPath, platform, locale)
  if srcDir:
    print("packing...")
    makePackage(srcDir, platform, locale)
  print

if __name__ == "__main__":
  main()

