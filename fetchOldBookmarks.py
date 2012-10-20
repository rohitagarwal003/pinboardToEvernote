#!/usr/bin/python
from credentials import *	#This imports PinboardAPIToken and DiffbotToken
import urllib, urllib2, json
from xml.dom.minidom import *

def getRecentBookmarks(auth_token):
	"""
	Takes the pinboard auth_token (which is of the form username:alphanumericString)
	Returns a list of (href, title, extended) for recent bookmarks.
	"""
	url = "https://api.pinboard.in/v1/posts/recent?auth_token=%s" % (auth_token)
	rawXML = urllib2.urlopen(url)
	parsedXML = xml.dom.minidom.parse(rawXML)
	bookmarkList = []
	for post in parsedXML.getElementsByTagName("post"):
		href = post.getAttribute("href")
		title = post.getAttribute("description")
		extended = post.getAttribute("extended")
		bookmark = (href, title, extended)
		bookmarkList.append(bookmark)
	return bookmarkList

def extractArticle(token, url):
	"""
	Takes the Diffbot developer token and the url of the article to be extracted.
	Returns the text of the article.
	"""
	url = urllib.quote(url)
	request = "http://www.diffbot.com/api/article?token=%s&url=%s" % (token, url)
	responseJSON = urllib2.urlopen(request)
	responseDict = json.load(responseJSON)
	return responseDict["text"]

if __name__ == '__main__':
	recentBookmarkList = getRecentBookmarks(PinboardAPIToken)
	for bookmark in recentBookmarkList:
		print bookmark[0]
		print bookmark[1]
		print extractArticle(DiffbotToken, bookmark[0])
		print "--------------------------------------------------"
		print
