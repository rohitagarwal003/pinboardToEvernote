#!/usr/bin/python

import traceback
import datetime
import argparse
from credentials import *
from pinboardHelper import *
from diffbotHelper import *
from sanitize import *
from evernoteHelper import *


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--sandbox", action="store_true", help="Store notes in a test account at sandbox.evernote.com instead of your main account at www.evernote.com. Use this option when you are testing the utility.")
	parser.add_argument("-n", "--notebook-name", metavar="NOTEBOOK", help="Store the bookmarks in the notebook named NOTEBOOK. If no notebook is specified then bookmarks are stored in the default notebook. If NOTEBOOK doesn't exist, then bookmarks are stored in the default notebook.")
	parser.add_argument("-t", "--tag", metavar="TAG", help="Retrieve only those bookmarks from pinboard which are tagged TAG.")
	args = parser.parse_args()

	print "Fetching bookmarks from Pinboard..."
	try:
		f = open("lastUpdate.txt", "r")
		fromdt = f.read().strip()
		f.close()
		firstUse = False
		print "Last fetched on: %s" % fromdt
	except IOError:
		# If lastUpdate.txt doesn't exist.
		# It means that the program is being run for the first time.
		# So get all bookmarks.
		print "Last fetched on: Never"
		firstUse = True

	try:
		if firstUse:
			if args.tag:
				bookmarkList = getAllBookmarksTagged(PinboardAPIToken, args.tag)
			else:
				bookmarkList = getAllBookmarks(PinboardAPIToken)
		else:
			if args.tag:
				bookmarkList = getBookmarksFromDateTagged(PinboardAPIToken, fromdt, args.tag)
			else:
				bookmarkList = getBookmarksFromDate(PinboardAPIToken, fromdt)
	except:
		print "Fetching bookmarks from Pinboard failed."
		traceback.print_exc()
		print
		exit(1)

	# We have fetched bookmarks uptill now.
	todt = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

	totalBookmarks = len(bookmarkList)
	notesCreated = 0
	diffbotErrors = 0
	sanitizeErrors = 0
	evernoteErrors = 0

	print "Total bookmarks = " + str(totalBookmarks)

	try:
		print "Initializing EvernoteHelper..."
		if args.sandbox:
			evernoteHelper = EvernoteHelper(EvernoteDeveloperToken, production=False)
		else:
			evernoteHelper = EvernoteHelper(EvernoteDeveloperToken, production=True)
	except:
		print "Creating EvernoteHelper failed."
		traceback.print_exc()
		print
		exit(1)

	failedURLs = open("failedURLs.txt", "a")

	print
	for bookmark in reversed(bookmarkList):

		try:
			print "Extracting article using Diffbot..."
			html = extractArticle(DiffbotToken, bookmark[0], html=True)
		except:
			print "Extracting article using Diffbot failed."
			print bookmark[0]
			failedURLs.write(bookmark[0] + "\n")
			traceback.print_exc()
			print
			diffbotErrors += 1
			continue

		try:
			print "Converting article from HTML to ENML..."
			enml = sanitize(html)
		except:
			print "Converting article from HTML to ENML failed."
			print bookmark[0]
			failedURLs.write(bookmark[0] + "\n")
			traceback.print_exc()
			print
			sanitizeErrors += 1
			continue

		try:
			print "Storing note in Evernote..."
			evernoteHelper.sendToEvernote(bookmark[1], bookmark[0], enml, notebookName=args.notebook_name)
		except:
			print "Storing note in Evernote failed."
			print bookmark[0]
			failedURLs.write(bookmark[0] + "\n")
			traceback.print_exc()
			print
			evernoteErrors += 1
			continue

		notesCreated += 1

	failedURLs.close()

	# Update the lastUpdate time.
	f = open("lastUpdate.txt", "w")
	f.write(todt)
	f.close()

	print
	print "Total bookmarks = " + str(totalBookmarks)
	print "Total number of notes created = " + str(notesCreated)
	print "Diffbot Errors = " + str(diffbotErrors)
	print "Sanitize Errors = " + str(sanitizeErrors)
	print "Evernote Errors = " + str(evernoteErrors)
	print

if __name__ == "__main__":
	main()
