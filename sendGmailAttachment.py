#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 11:18:13 2014

@author: emilio based on Rodrigo Coutinho 
http://kutuma.blogspot.com.es/2007/08/sending-emails-via-gmail-with-python.html
"""

import os
import sys
import json
import shutil
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

# Load data from json file
jsonFile=open('config.json')
jsonData = json.load(jsonFile)
jsonFile.close()

user = jsonData['user']
pwd = jsonData['pwd']

tmpFolder = sys.path[0] +'/tmp/'
analysedFolder = sys.path[0] + '/analysed/'
attFolder = sys.path[0] + '/attachments/'
sentFolder = sys.path[0] + '/sent/'

def gmailWithAttachment(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = user
   msg['To'] = to
#   msg['Subject'] = "Your"
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(user, pwd)
   mailServer.sendmail(user, to, msg.as_string())
   mailServer.close()

# The list of analysed files we have to send attached
analysedList = []
analysedSgfFiles = os.listdir(analysedFolder)
for sgfFile in analysedSgfFiles:
    analysedList.append(sgfFile)
print 'analysedList'
print analysedList
    
# The list of emails-sgfFiles
dataList = []
dataFile = open(sys.path[0] + '/data_file.txt','r')
for line in dataFile:
    dataList.append(line)
print 'dataList'    
print dataList

for analysedFile in analysedSgfFiles:
    for data in dataList:
        if data.split(' ')[0].split('.')[0] in analysedFile:
            print 'Coincidence!'
            print data.split(' ')[0]
            print analysedFile
            print data.split(' ')[1]
            gmailWithAttachment(data.split(' ')[1],
            "Your analysed sgf",
            "This is the result of the analysis of your game by gnugo",
            "analysed/" + analysedFile)
            # And now we move the just sent file to the sent folder
            shutil.move(analysedFolder + analysedFile, sentFolder + analysedFile)
