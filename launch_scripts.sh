#!/bin/bash

PATH=/usr/bin:/bin:/sbin:/usr/games/

cd ~/soft/GoAnalyser
./downloadSgfAttached.py
./analyseSgfFiles.py > /home/emilio/ipsender.log 2>&1
#./analyseSgfFiles.py
./sendGmailAttachment.py
