#!/usr/bin/python
import urllib
import urllib2
import json


def extractArticle(token, url, html=True):
	"""
	Takes the Diffbot developer token and the url of the article to be extracted.
	Returns the text of the article.
	"""
	if not token:
		print "Please fill in your diffbot developer token"
		print "You can get a free token from http://www.diffbot.com/plans/free"
		exit(1)

	url = urllib.quote(url)
	if html:
		request = "http://www.diffbot.com/api/article?token=%s&url=%s&html" % (token, url)
		responseJSON = urllib2.urlopen(request)
		responseDict = json.load(responseJSON)
		try:
			return responseDict["html"]
		except KeyError:
			return ""
	else:
		request = "http://www.diffbot.com/api/article?token=%s&url=%s" % (token, url)
		responseJSON = urllib2.urlopen(request)
		responseDict = json.load(responseJSON)
		try:
			return responseDict["text"]
		except KeyError:
			return ""
