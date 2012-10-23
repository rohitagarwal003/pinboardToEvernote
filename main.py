#!/usr/bin/python

import traceback, datetime
from credentials import *
from pinboardHelper import *
from diffbotHelper import *
from sanitize import *
from evernoteHelper import *

def main():
	try:
		if len(sys.argv) == 1:
			bookmarkList = getTodaysBookmarks(PinboardAPIToken)
		elif len(sys.argv) == 2:
			if sys.argv[1] == "recent":
				bookmarkList = getRecentBookmarks(PinboardAPIToken)
			elif sys.argv[1] == "all":
				bookmarkList = getAllBookmarks(PinboardAPIToken)
			elif sys.argv[1] == "today":
				bookmarkList = getTodaysBookmarks(PinboardAPIToken)
			else:
				print "Invalid argument"
				exit(1)
		elif len(sys.argv) == 4:
			fromdt = datetime.date(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
			bookmarkList = getBookmarksFromDate(PinboardAPIToken, fromdt)
		else:
			print "Wrong Number of arguments"
			exit(1)
	except:
		print "Fetching bookmarks from Pinboard failed."
		traceback.print_exc()
		print
		exit(1)

	notesCreated = 0
	for bookmark in bookmarkList:

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

if __name__ == "__main__":
	main()
