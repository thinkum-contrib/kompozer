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

# Input = raw binaries:
# build/
#   raw/
#     linux-i686/           macosx/                  win32/
#       kompozer/             KompoZer.app/            KompoZer/
#         chrome/               Contents/                chrome/
#         defaults/               MacOS/                 defaults/
#         dictionaries/             chrome/              dictionaries/
#                                   defaults/
#                                   dictionaries/
#                                 Resources/
#                                   en.lproj      

# Output = localized binaries:
# build/
#   test/                [VERSION]/
#     linux-i686/          linux-i686/
#       %AB_CD%              kompozer-%VERSION%.%AB_CD%-gcc4.2-i686.tar.gz
#         kompozer/        macosx/
#     macosx/                kompozer-%VERSION%.%AB_CD%-macosx-universal.dmg
#       %AB_CD%            win32/
#         KompoZer.app/      exe/
#     win32/                   kompozer-%VERSION%.%AB_CD%-win32.exe
#       %AB_CD%              zip/
#         kompozer/            kompozer-%VERSION%.%AB_CD%-win32.zip

VERSION = "0.8b3"

# preferences: adapt these lines to your config
CHROME_ROOT     = "chrome/"
L10N_ROOT       = "l10n/"
MYSPELL_ROOT    = "myspell/"

BUILD_ROOT      = "build/"
BUILD_RAW       = "build/raw/"
BUILD_TEST      = "build/test/"

LINUX_RAW       = BUILD_RAW + "linux-i686/kompozer/"
MACOSX_RAW      = BUILD_RAW + "macosx/KompoZer.app/"
WIN32_RAW       = BUILD_RAW + "win32/KompoZer/"

# shell access, check the value of "DEBUG"
DEBUG = 0
def shell(cmd):
  if DEBUG:
    print(cmd)
  else:
    os.system(cmd)


###############################################################################
#                                                                             #
#     l10n converters                                                         #
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
    print("unsupported platform: use 'linux', 'macosx' or 'win'")
    return
  chromeDir  = binDir + "chrome/"
  prefsDir   = binDir + "defaults/pref/"
  profileDir = binDir + "defaults/profile/"
  dictDir    = binDir + "dictionaries/"
  print("building " + destDir)

  # create a directory for the new localized build
  if os.path.exists(destDir):
    shell("rm -rf " + destDir)
  shell("mkdir -p " + destDir)
  shell("cp -R " + srcDir + " " + destDir)

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
    os.chdir(destDir + "Contents/Resources/")
    # Catalan and Hungarian are specific cases
    if (locale == "ca"):
      shell("mv en.lproj ca-AD.lproj")
    elif (locale == "hu"):
      shell("mv en.lproj hu-HU.lproj")
    else:
      shell("mv en.lproj " + locale + ".lproj")

  # change locale in all.js
  os.chdir(prefsDir)
  shell("sed -i s/en-US/" + locale + "/g all.js")

  # some locales require specific char encodings
  sedAcceptCharsets = "sed -i s/iso-8859-1,\*,utf-8/"
  sedCustomCharset  = "sed -i s/ISO-8859-1/"
  if (locale == "ja"):
    shell(sedAcceptCharsets + "Shift_JIS,\*,utf-8/g all.js")
    shell(sedCustomCharset  + "Shift_JIS/g editor.js")
  elif (locale == "zh-CN" or locale == "zh-TW" or locale == "hsb"):
    shell(sedAcceptCharsets + "utf-8,\*,iso-8859-1/g all.js")
    shell(sedCustomCharset  + "UTF8/g editor.js")
  elif (locale == "hu" or locale == "pl"):
    shell(sedAcceptCharsets + "iso-8859-2,\*,utf-8/g all.js")
    shell(sedCustomCharset  + "ISO-8859-2/g editor.js")
  elif (locale == "ru"):
    shell(sedAcceptCharsets + "Windows-1251,\*,utf-8/g all.js")
    shell(sedCustomCharset  + "Windows-1251/g editor.js")

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
    # hdiutil create -srcfolder "KompoZer.app" -volname "KompoZer ab(-CD)" kompozer-0.8.ab(-CD).mac-universal.dmg -format UDZ0 -imagekey zlib-level=9
    srcfolder = ' -srcfolder "' + srcDir + '"'
    volname = ' -volname "KompoZer "' + locale + '"'
    options = ' -format UDZ0 -imagekey zlib-level=9'
    dmgFile = ' ' + baseDir + baseFile
    shell("hdiutil create" + srcfolder + volname + dmgFile + options)

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
    print("unsupported platform: use 'linux', 'macosx' or 'win'")
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
  platform = "linux"
  locale = "fr"
  srcDir = makeBinary(LINUX_RAW, platform, locale)
  if srcDir:
    makePackage(srcDir, platform, locale)

if __name__ == "__main__":
  main()

