#!/usr/bin/python
# author      : Fabien Cazenave <kaze@kompozer.net>
# purpose     : release utility script for KompoZer 0.8
# requires    : bash + Python 2.5
#               successfully tested on GNU/Linux and MacOS X
#               does not work on Windows yet (even with Cygwin)
# last update : 2010-03-01

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
LOCALES = ["ca", "cs", "da", "de", "en-US", "eo", "es-ES", "fi", "fr", "hu", \
           "hsb", "it", "ja", "nl", "pl", "pt-PT", "ru", "sl", "zh-CN", "zh-TW"]


###############################################################################
#                                                                             #
# INPUT: en-US raw binaries                                                   #
# -------------------------                                                   #
#                                                                             #
#      __LINUX__              __MacOSX__                __WIN32__             #
#                                                                             #
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
#   bin/                 [version]/                                           #
#     linux-i686/          linux-i686/                                        #
#       @ab-CD@              kompozer-@version@.@ab-CD@-gcc4.2-i686.tar.gz    #
#         kompozer/        macosx/                                            #
#     macosx/                kompozer-@version@.@ab-CD@-mac-universal.dmg     #
#       @ab-CD@            win32/                                             #
#         KompoZer.app/      exe/                                             #
#     win32/                   kompozer-@version@.@ab-CD@-win32.exe           #
#       @ab-CD@              zip/                                             #
#         KompoZer/            kompozer-@version@.@ab-CD@-win32.zip           #
#                                                                             #
###############################################################################

# preferences: adapt these lines to your config
CHROME_ROOT  = "chrome/"
MYSPELL_ROOT = "myspell/"
BUILD_ROOT   = "build/"
BUILD_TEST   = "build/bin/"
BUILD_JAR    = "build/jar/"

# Requirements to build win32 installers:
#  * Inno Setup 5 has to be installed (works through Wine on Linux and MacOSX)
#  * 'kompozer.iss' has to match the BUILD_[ROOT|TEST] settings above
INNO_SETUP  = "wine ~/.PlayOnLinux/wineprefix/InnoSetup/drive_c/Program\ Files/Inno\ Setup\ 5/ISCC.exe"
#INNO_SETUP = "wine ~/.wine/drive_c/Program\ Files/Inno\ Setup\ 5/ISCC.exe"
#INNO_SETUP = "ISCC.exe"       # when using on Windows
#INNO_SETUP = 0                # set to 0 to disable InnoSetup


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
# ('sed -i' doesn't work exactly on MacOSX as it does on GNU/Linux)
def replaceInFile(findStr, replaceStr, filePath):
  sed = "sed 's/" + findStr + "/" + replaceStr + "/g' "
  shell(sed + filePath + " > " + filePath + "~")
  shell("mv " + filePath + "~ " + filePath)

# Clone the 'srcPath' directory as a child of 'destPath'
# ('cp -r' doesn't work exactly on MacOSX as it does on GNU/Linux)
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
  shell("cp -RL " + srcPath + "/* " + destDir)
  return destDir + "/"


###############################################################################
#                                                                             #
#     Package utilities                                                       #
#                                                                             #
###############################################################################

# create localized binary
def makeBinary(srcDir, platform, locale):
  jarFile = BUILD_JAR + locale + ".jar"
  if not os.path.exists(jarFile):
    print(jarFile + " is missing, please run './convert-locales make " + locale + "' first.")
    return 0

  # set base directories
  cwd = os.getcwd() + "/"
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
  os.chdir(chromeDir)
  sed = "sed s/en-US/" + locale + "/g "
  shell(sed + "en-US.manifest > " + locale  + ".manifest")
  os.chdir(cwd)
  shell("rm " + chromeDir + "en-US.*")
  shell("cp " + jarFile + " " + chromeDir)

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
  elif (locale == "zh-CN" or locale == "zh-TW" or locale == "hsb" or locale == "eo"):
    replaceInFile(acceptCharsets, "utf-8,\*,iso-8859-1",   "all.js")
    replaceInFile(customCharset,  "UTF8",                  "editor.js")
  elif (locale == "cs" or locale == "hu" or locale == "pl" or locale == "sl"):
    replaceInFile(acceptCharsets, "iso-8859-2,\*,utf-8",   "all.js")
    replaceInFile(customCharset,  "ISO-8859-2",            "editor.js")
  elif (locale == "ru"):
    replaceInFile(acceptCharsets, "Windows-1251,\*,utf-8", "all.js")
    replaceInFile(customCharset,  "Windows-1251",          "editor.js")

  # disable line wrapping for Asian languages (= 72 chars by default)
  if (locale == "ja" or locale == "zh-CN" or locale == "zh-TW"):
    replaceInFile(" 72);", " 0);", "editor.js")

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
    tarFile = baseDir + baseFile + ".gcc4.2-i686.tar.gz"
    shell("mkdir -p " + baseDir)
    if os.path.exists(tarFile):
      shell("rm " + tarFile)
    shell("tar -chzf " + tarFile + " kompozer")

  # MacOSX: dmg image
  elif (platform == "mac"):
    baseDir += "/macosx/"
    baseFile += ".mac-universal.dmg"
    shell("mkdir -p " + baseDir)
    srcfolder = ' -srcfolder "' + srcDir + '"'
    volname = ' -volname "KompoZer ' + locale + '" '
    options = ' -format UDZO -imagekey zlib-level=9 '
    dmgFile = baseDir + baseFile
    if os.path.exists(dmgFile):
      shell("rm " + dmgFile)
    shell("hdiutil create -srcfolder ." + volname + dmgFile + options)

  # Win32: zip archive
  elif (platform == "win"):
    baseDir += "/win32/"
    zipFile = baseDir + "zip/" + baseFile + ".win32.zip"
    shell("mkdir -p " + baseDir + "zip")
    if os.path.exists(zipFile):
      shell("rm " + zipFile)
    shell("zip -rq " + zipFile + " KompoZer")

  # mismatch
  else:
    print("unsupported platform")
    return

  # done
  os.chdir(cwd)
  return

# pack localized win32 installer
def makeInnoSetup(srcDir, locale):
  langDict = {                      \
    'bg'   : 'Bulgarian',           \
    'ca'   : 'Catalan',             \
    'cs'   : 'Czech',               \
    'da'   : 'Danish',              \
    'de'   : 'German',              \
    'en-US': 'English',             \
    'eo'   : 'Esperanto',           \
    'es-AR': 'Spanish',             \
    'es-ES': 'Spanish',             \
    'es-MX': 'Spanish',             \
    'fr'   : 'French',              \
    'fi'   : 'Finnish',             \
    'hu'   : 'Hungarian',           \
    'hsb'  : 'German',              \
    'it'   : 'Italian',             \
    'ja'   : 'Japanese',            \
    'ko'   : 'Korean',              \
    'nl'   : 'Dutch',               \
    'pl'   : 'Polish',              \
    'pt-BR': 'BrazilianPortuguese', \
    'pt-PT': 'Portuguese',          \
    'ru'   : 'Russian',             \
    'sk'   : 'Slovak',              \
    'sl'   : 'Slovenian',           \
    'tr'   : 'Turkish',             \
    'zh-CN': 'ChineseSimplified',   \
    'zh-TW': 'ChineseTraditional'   \
  }

  # get proper InnoSetup messages file
  msgName = langDict[locale].lower()
  if locale == "en-US":
    msgFile = "Default.isl"
  else:
    msgFile = "Languages\\\\" + langDict[locale] + ".isl"

  # make a temporary InnoSetup script
  issFile = "kompozer-" + locale + ".iss"
  shell("cp kompozer.iss " + issFile)
  replaceInFile("@LOCALE@",   locale,   issFile)
  replaceInFile("@VERSION@",  VERSION,  issFile)
  replaceInFile("@MSGNAME@",  msgName,  issFile)
  replaceInFile("@MSGFILE@",  msgFile,  issFile)

  # start InnoSetup compiler
  shell(INNO_SETUP + " /Q " + issFile)
  shell("rm " + issFile)


###############################################################################
#                                                                             #
#     Command-line handling                                                   #
#                                                                             #
###############################################################################

# main: parse command-line arguments
def main():
  if len(sys.argv) < 2: # not enough arguments
    print("usage: ./release.py (path/to/kompozer/directory) [locales]")
    print("  if [locales] is not specified, all supported locales will be built:")
    print("       " + ", ".join(LOCALES))
    return

  # get binary directory and target platform
  srcPath = sys.argv[1]
  if srcPath[-1:] == "/":
    srcPath = srcPath[0:-1]
  if os.path.basename(srcPath) == "KompoZer.app":
    platform = "mac"
  elif os.path.exists(srcPath + "/kompozer-bin"):
    platform = "linux"
  elif os.path.exists(srcPath + "/kompozer.exe"):
    platform = "win"
    # check MSVC70 DLLs (it's easy to forget them...)
    hasMSVC7 = os.path.exists(srcPath + "/msvcp70.dll") \
           and os.path.exists(srcPath + "/msvcr70.dll")
    if not hasMSVC7:
      print("MSVC7 DLLs are missing, can't build Windows versions.")
      return
  else:
    print("not a kompozer binary.")
    return

  # get the list of the locales to build
  if (len(sys.argv) > 2):
    locales = sys.argv[2:]
  else:              # build all locales
    locales = LOCALES

  # build
  for locale in locales:
    print
    print("building kompozer-" + VERSION + "." + locale + " (" + platform + ")...")
    srcDir = makeBinary(srcPath, platform, locale)
    if srcDir:
      print("  packing...")
      makePackage(srcDir, platform, locale)
      if INNO_SETUP and (platform == "win"):
        print("  InnoSetup...")
        makeInnoSetup(srcDir + "\KompoZer", locale)

  # done
  print

if __name__ == "__main__":
  main()

