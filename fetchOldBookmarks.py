#!/usr/bin/python
from credentials import *	#This imports PinboardAPIToken
import urllib2
from xml.dom.minidom import *

def getRecentBookmarks(auth_token):
	url = "https://api.pinboard.in/v1/posts/recent?auth_token=%s" % (auth_token)
	rawXML = urllib2.urlopen(url)
	parsedXML = xml.dom.minidom.parse(rawXML)
	for post in parsedXML.getElementsByTagName("post"):
		href = post.getAttribute("href")
		title = post.getAttribute("description")
		extended = post.getAttribute("extended")
		print href
		print title
		print extended
		print

if __name__ == '__main__':
	getRecentBookmarks(PinboardAPIToken)
