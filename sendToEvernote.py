#!/usr/bin/python

import traceback
from credentials import *
from pinboard import *
from diffbot import *
from sanitize import *
from evernoteHelper import *

try:
	recentBookmarkList = getRecentBookmarks(PinboardAPIToken)
except:
	print "Fetching bookmarks from Pinboard failed."
	traceback.print_exc()
	print
	exit(1)

notesCreated = 0
for bookmark in recentBookmarkList:

	try:
		html = extractArticle(DiffbotToken, bookmark[0], html=True)
	except:
		print "Extracting article using Diffbot failed."
		print bookmark[0]
		traceback.print_exc()
		print
		continue
		#exit(1)

	try:
		enml = sanitize(html)
	except:
		print "Converting article from HTML to ENML failed."
		print bookmark[0]
		traceback.print_exc()
		print
		continue
		#exit(1)

	#print
	#print enml
	#print
	#print "length of enml is " + str(len(enml))
	#print "type of enml is " + str(type(enml))

	try:
		sendToEvernote(bookmark[1], bookmark[0], enml, EvernoteDeveloperToken)
	except:
		print "Storing note in Evernote failed."
		print bookmark[0]
		print enml
		print
		traceback.print_exc()
		print
		continue
		#exit(1)

	notesCreated += 1

print "Total number of notes created = " + str(notesCreated)
