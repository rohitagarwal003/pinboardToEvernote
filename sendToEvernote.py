# To run (Unix):
#   export PYTHONPATH=./lib; python sendToEvernote.py

import sys
import hashlib
import binascii
import time
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

import traceback
from credentials import *
from fetchOldBookmarks import *
from sanitize import *

# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account. To get a developer token, visit 
# https://sandbox.evernote.com/api/DeveloperToken.action
authToken = EvernoteDeveloperToken

if authToken == "your developer token":
    print "Please fill in your developer token"
    print "To get a developer token, visit https://sandbox.evernote.com/api/DeveloperToken.action"
    exit(1)

# Initial development is performed on our sandbox server. To use the production 
# service, change "sandbox.evernote.com" to "www.evernote.com" and replace your
# developer token above with a token from 
# https://www.evernote.com/api/DeveloperToken.action
evernoteHost = "sandbox.evernote.com"
userStoreUri = "https://" + evernoteHost + "/edam/user"

userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
userStore = UserStore.Client(userStoreProtocol)

versionOK = userStore.checkVersion("Evernote EDAMTest (Python)",
                                   UserStoreConstants.EDAM_VERSION_MAJOR,
                                   UserStoreConstants.EDAM_VERSION_MINOR)
print "Is my Evernote API version up to date? ", str(versionOK)
print ""
if not versionOK:
    exit(1)

# Get the URL used to interact with the contents of the user's account
# When your application authenticates using OAuth, the NoteStore URL will
# be returned along with the auth token in the final OAuth request.
# In that case, you don't need to make this call.
noteStoreUrl = userStore.getNoteStoreUrl(authToken)

noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
noteStore = NoteStore.Client(noteStoreProtocol)

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
		traceback.print_exc()
		print
		#continue
		exit(1)

	enml = sanitize(html).toxml()
	print
	print enml
	print
	print "length of enml is " + str(len(enml))
	print "type of enml is " + str(type(enml))
	# To create a new note, simply create a new Note object and fill in 
	# attributes such as the note's title.
	note = Types.Note()
	note.title = bookmark[1]
	#note.attributes = Types.NoteAttributes()
	#note.attributes.sourceURL = bookmark[0]
	#print note

	# The content of an Evernote note is represented using Evernote Markup Language
	# (ENML). The full ENML specification can be found in the Evernote API Overview
	# at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
	note.content = '<?xml version="1.0" encoding="UTF-8"?>'
	note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
	note.content += enml.encode('ascii', 'xmlcharrefreplace')

	print
	print "Creating a new note in the default notebook"
	print

	# Finally, send the new note to Evernote using the createNote method
	# The new Note object that is returned will contain server-generated
	# attributes such as the new note's unique GUID.
	try:
		createdNote = noteStore.createNote(authToken, note)
	except:
		print "Storing note in Evernote failed."
		traceback.print_exc()
		print
		continue
		#exit(1)

	print "Successfully created a new note with GUID: ", createdNote.guid
	notesCreated += 1

print "Total number of notes created = " + str(notesCreated)
