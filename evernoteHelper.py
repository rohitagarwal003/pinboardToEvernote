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

class EvernoteHelper:

	def __init__(self, authToken, production=False):
		if not authToken:
			print "Please fill in your developer token"
			print "To get a developer token, visit"
			print "https://sandbox.evernote.com/api/DeveloperToken.action (for testing and development)"
			print "OR"
			print "https://www.evernote.com/api/DeveloperToken.action (for production)"
			exit(1)

		if production:
			self.evernoteHost = "www.evernote.com"
		else:
			self.evernoteHost = "sandbox.evernote.com"

		self.authToken = authToken
		self.userStoreUri = "https://" + self.evernoteHost + "/edam/user"
		self.userStoreHttpClient = THttpClient.THttpClient(self.userStoreUri)
		self.userStoreProtocol = TBinaryProtocol.TBinaryProtocol(self.userStoreHttpClient)
		self.userStore = UserStore.Client(self.userStoreProtocol)

		self.noteStoreUrl = self.userStore.getNoteStoreUrl(authToken)
		self.noteStoreHttpClient = THttpClient.THttpClient(self.noteStoreUrl)
		self.noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(self.noteStoreHttpClient)
		self.noteStore = NoteStore.Client(self.noteStoreProtocol)

	def sendToEvernote(self, title, sourceURL, enml):

		# To create a new note, simply create a new Note object and fill in attributes
		note = Types.Note()
		note.title = title.encode('ascii', 'xmlcharrefreplace')
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
		createdNote = self.noteStore.createNote(self.authToken, note)

		print "Successfully created a new note with GUID: ", createdNote.guid
