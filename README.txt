This group of scripts read the sgf files sent to myaccount@myaccount.com, analyse them
wtih the help of gnugo and send the result of the analysis to the original email address.

SGF are "smart game format", a file format to store Go records: http://senseis.xmp.net/?SmartGameFormat

Gnugo is a free software Go engine: https://en.wikipedia.org/wiki/GNU_Go

A json file is needed with the info:
{
  "user": "myaccount@myaccount.com",
  "pwd": "password"
}


Important folders:
-attachments: the folder where the original sgf files are downloaded
-tmp: the folder where the analysed files are stored during the analysis process
-analysed: the folder where finally the analysed files are stored
-sent: where the analysed files are finally placed after they are sent to their
original senders

Scripts:
-downloadSgfAttached.py: downloads the attached files and stores them in /attachments.
It also populates the data_file.txt with the next format:
one_sgf_file one_email_address@myaddress.com
another_sgf_file another_email_address@myaddress.com
-analyseSgfFiles.py: uses the sgf files in /attachments and analyse them, just one per
time, no matter how many sgf files there are, in order to not to overload the cpu. It
leaves the result of the analysis in /analysed
-sendGmailAttachment.py: it takes the files in /analysed and with the info stored in
data_file.txt sends an email with the analysed files attached

Known issues:
-The "subject" field remains empty when the email with the analysed game is received
-Folders analysed, attachments, tmp and sent must be created before launching the scripts
-Only for linux based systems (makes use of linux commands like 'ps')
