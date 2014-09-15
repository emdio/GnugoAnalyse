#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 17:29:41 2014

@author: emilio
"""

# Goes to the "attachments" folder and if it isn't empty and gnugo is not running
# it'll take one sgf file, analyse it and place the result in the
# "analysed" folder

import os
import shutil
import sys
import subprocess


tmpFolder = sys.path[0] +'/tmp/'
analysedFolder = sys.path[0] + '/analysed/'
attFolder = sys.path[0] + '/attachments/'
level = '1'     # Anlysis level for gnugo

def isGnugoRunning():
    gnugoIsRunning = False
    procList = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
    procList = procList.split('\n')
    for proc in procList:
        if 'gnugo' in proc:
            gnugoIsRunning = True
    return gnugoIsRunning

if isGnugoRunning():
    print 'Gnugo is already running'
    exit()
else:
    print 'Gnugo is not running so we will search for a game to analyse'
    sgfFiles = os.listdir(attFolder)
    # We only want to analyse one file each time we run this script in order
    # to not to overload the cpu
    if len(sgfFiles) != 0:
        sgfFile = sgfFiles[0]
        if 'sgf' in sgfFile:
            print 'There is a sgf file to analyse:', sgfFile
            sgfAnnotatedFileName = sgfFile.split('.')
            sgfAnnotatedFileName = sgfAnnotatedFileName[0] + '_annotated'  + '_gnugo_lvl-' + level + '.' + sgfAnnotatedFileName[1]
            print 'Starting the analysis...'            
            subprocess.Popen(['gnugo', '-l', attFolder + sgfFile, '--output-flags', 'dv', '--level', level, '--replay', 'both', '--never-resign', '-o', tmpFolder + sgfAnnotatedFileName], stdout=subprocess.PIPE).communicate()[0]
            # Once the file is analysed we move the resulting file to the final folder
            shutil.move(tmpFolder + sgfAnnotatedFileName, analysedFolder + sgfAnnotatedFileName)
            # And remove the original file in order to not to analyse it again
            os.remove(attFolder + sgfFile)
    else:
        print 'There is no file to analyse...'
        exit()