#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 20:11:34 2014

@author: emilio

http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail

"""

import os
import sys
import email
import json
#import getpass
import imaplib


attFolder = sys.path[0] + '/attachments/'

def saveFileEmail(filename, emailAddress):
    dataFile = open('data_file.txt','a')
    # Write the data
    dataFile.write(filename + ' ')
    dataFile.write(emailAddress + '\n')
    dataFile.close()

# Load data from json file
jsonFile=open('config.json')
jsonData = json.load(jsonFile)
jsonFile.close()

user = jsonData['user']
pwd = jsonData['pwd']

# Connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
m.select("INBOX")
resp, items = m.search(None, "UNSEEN")
items = items[0].split() # getting the mails id

if len(items) == 0:
    print 'There is no new email'
    exit()

for emailId in items:
    resp, data = m.fetch(emailId, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    emailBody = data[0][1] # getting the mail content
    mail = email.message_from_string(emailBody) # parsing the mail content to get a mail object

    #Check if any attachments at all
    if mail.get_content_maintype() != 'multipart':
        print 'There is no new attachment...'
        continue

    print "["+mail["From"]+"] :" + mail["Subject"]
    emailAddress = mail['From']
    emailAddress = emailAddress[emailAddress.find("<")+1:emailAddress.find(">")]

    # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
    for part in mail.walk():
        # multipart are just containers, so we skip them
        if part.get_content_maintype() == 'multipart':
            continue

        # is this part an attachment ?
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        counter = 1
        
        # Is it a sgf file?
        if not 'sgf'in filename and not 'SGF' in filename:
            print 'The attachment is not an SGF file'
            continue

        # if there is no filename, we create one with a counter to avoid duplicates
        if not filename:
            filename = 'part-%03d%s' % (counter, 'bin')
            counter += 1

        # Now we save in a txt file the file name and the email address. This txt file
        # will be used by another script to send the analysed games to its destinies
        saveFileEmail(filename, emailAddress)

        attFolder = os.path.join(attFolder, filename)
        
        #Check if its already there
        if not os.path.isfile(attFolder) :
            # finally write the stuff
            fp = open(attFolder, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()