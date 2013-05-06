import urllib, urllib2, cookielib
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Page:
	fields = {}
	url = None
	connection = None
	html = None # BeautifulSoup object
	cookieJar = None
	opener = None
	response = None
	
	def __init__(self, url, cj):
		self.url = url
		self.cookieJar = cj
		
	def connect(self):
		print "---> Connecting to %s" % (self.url,)
		
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
		self.opener.addheaders.append(('User-agent', 'Mozilla/4.0'))
		
		if self.fields:
			data = urllib.urlencode(self.fields)
			self.response = self.opener.open(self.url, data)
			print "-----> Sending data:"
			for c in self.fields.keys():
				print "-------> %s = %s" % (c, self.fields[c][:20])
		else:
			self.response = self.opener.open(self.url)
			
		self.html = BeautifulSoup(self.response.read())

		# save the pages for diagnostic info
		save = open(re.sub(r'\W+', '', self.html.title.string) + '.html', 'w')
		save.write(str(self.html))
		save.close()

	
	def acquireHiddenFields(self):
		# search the page for hidden POST fields
		
		self.fields = {}
		
		for field in self.html('input', type='hidden'):
			name = field['name']
			value = ''
			try:
				value = field['value']
			except KeyError:
				value = ''
			
			self.fields[name] = value
		
	def acquireTestCentreId(self):
		# get the test centre ID from the page
		centreId = ''
		
		field = self.html.find('input', { 'name': 'rblTestCentres' })
		if field:	
			try:
				centreId = field['value']
			except KeyError:
				centreId = ''
				
		return centreId
		

class SlotsPage(Page):
		
	def acquireDateSlots(self):
		# scrape the html for dates and return them
		# as a list
		
		dtList = []
		
		for slot in self.html('input', { 'name': 'rblSlots' }):
			dateString = None
			try:
				dateString = slot['value']
			except:
				dateString = None
			
			if dateString:
				# parse the date string
				dt = datetime.strptime(dateString, '%A %d %B %Y %I:%M%p')
				dtList.append(dt)
		
		return dtList
		











		