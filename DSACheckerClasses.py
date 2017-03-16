import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, http.cookiejar
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
		print("---> Connecting to %s" % (self.url,))
		               
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookieJar))
		self.opener.addheaders.append(('User-agent', 'Mozilla/4.0'))
		
		if self.fields:
			data = urllib.parse.urlencode(self.fields)
			binary_data = data.encode('ascii')
			self.response = self.opener.open(self.url, binary_data)
			print("-----> Sending data:")
			for c in list(self.fields.keys()):
				print("-------> %s = %s" % (c, self.fields[c][:20]))
		else:
			self.response = self.opener.open(self.url)
			
		self.html = BeautifulSoup(self.response.read(), "html.parser")

		# save the pages for diagnostic info
		# save = open(re.sub(r'\W+', '', self.html.title.string) + '.html', 'w')
		# save.write(str(self.html))
		# save.close()
		











		
