#!/usr/bin/python

import sys
import os
import hashlib
import binascii
import time

home = os.path.dirname(os.path.abspath(__file__))
evernoteLibraryPath = os.path.join(home, "lib")
sys.path.insert(0, evernoteLibraryPath)

import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

def sendToEvernote(title, sourceURL, enml, authToken, production=False):

	if not authToken:
	    print "Please fill in your developer token"
	    print "To get a developer token, visit"
	    print "https://sandbox.evernote.com/api/DeveloperToken.action (for testing and development)"
	    print "OR"
	    print "https://www.evernote.com/api/DeveloperToken.action (for production)"
	    exit(1)

	if production:
		evernoteHost = "www.evernote.com"
	else:
		evernoteHost = "sandbox.evernote.com"

	userStoreUri = "https://" + evernoteHost + "/edam/user"
	userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
	userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
	userStore = UserStore.Client(userStoreProtocol)

	noteStoreUrl = userStore.getNoteStoreUrl(authToken)
	noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
	noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
	noteStore = NoteStore.Client(noteStoreProtocol)

	# To create a new note, simply create a new Note object and fill in attributes
	note = Types.Note()
	note.title = title
	note.attributes = Types.NoteAttributes()
	note.attributes.sourceURL = sourceURL

	note.content = '<?xml version="1.0" encoding="UTF-8"?>'
	note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
	note.content += enml.encode('ascii', 'xmlcharrefreplace')

	print
	print "Creating a new note in the default notebook"
	print

	# Finally, send the new note to Evernote using the createNote method
	# The new Note object that is returned will contain server-generated
	# attributes such as the new note's unique GUID.
	createdNote = noteStore.createNote(authToken, note)

	print "Successfully created a new note with GUID: ", createdNote.guid
