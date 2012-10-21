import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from tidylib import *
from xml.dom.minidom import *
import re

def sanitize(html):
        document, errors = tidy_fragment(html, options={"drop-proprietary-attributes":1, "doctype":'omit'})	
	document, errors = tidy_document(document, options={"output-xhtml":1})	#xml.dom.minidom is an XML parser, not an HTML parser. Therefore, it doesn't know any HTML entities (only those which are common to both XML and HTML). So, when I was passing the document I got from earlier statement I got xml.parsers.expat.ExpatError: undefined entity.
	parsedDOM = xml.dom.minidom.parseString(document)
	documentElement = parsedDOM.documentElement
	removeProhibitedElements(documentElement)
	removeProhibitedAttributes(documentElement)
	return documentElement.getElementsByTagName("body")[0]

def removeProhibitedElements(documentElement):
	prohibitedTagNames = ["applet", "base", "basefont", "bgsound", "blink", "button", "dir", "embed", "fieldset", "form", "frame", "frameset", "head", "iframe", "ilayer", "input", "isindex", "label", "layer","legend", "link", "marquee", "menu", "meta", "noframes", "noscript", "object", "optgroup", "option", "param", "plaintext", "script", "select", "style", "textarea", "xml",] 
	for tagName in prohibitedTagNames:
		removeProhibitedElement(tagName, documentElement)

def removeProhibitedElement(tagName, documentElement):
	elements = documentElement.getElementsByTagName(tagName)
	for element in elements:
		p = element.parentNode
		p.removeChild(element)

def removeProhibitedAttributes(element):
	prohibitedAttributes = ["id", "class", "onclick", "ondblclick", "on*", "accesskey", "data", "dynsrc", "tabindex",]
	for attribute in prohibitedAttributes:
		try:
			element.removeAttribute(attribute)
		except xml.dom.NotFoundErr:
			pass
	try:
		if element.hasAttribute("href"):
			t = element.toxml()
			if re.search('href="http', t) or re.search('href="https', t):
				pass                                         
			else:
				element.removeAttribute("href")                  
	except:
		pass

	listOfChildren = element.childNodes                          
	for child in listOfChildren:                             
		if child.nodeType == 1:                              
			removeProhibitedAttributes(child)

