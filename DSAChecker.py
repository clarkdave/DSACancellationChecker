#!/usr/bin/python
"""

	DSA Checker
	For finding cancellations quickly and easily!
	
"""
import urllib, urllib2, cookielib, time, sys, os
from datetime import timedelta
from datetime import datetime
from bs4 import BeautifulSoup
from DSACheckerClasses import Page, SlotsPage

# this should point at the DSA login page
launchPage = 'https://driverpracticaltest.direct.gov.uk/login'

# the full licence number
licenceNumber = '**********'

# full theory certificate number
theoryNumber = '************'

# date theory test was passed (on certificate)
#theoryPassDate = ('2010', '01', '01')

# surname on driving licence
#surname = 'Foo'

# birth date
#birthDate = ('1990', '01', '01')

cookieJar = cookielib.CookieJar()

# these addresses will be mailed when a cancellation is found
emailAddresses = ['example@example.com']
emailSubject = "DSA Cancellations"
emailFrom = "no-reply@example.com"

# Put in your current test date in the format "Thursday 4 July 2013 2:00pm"; you will be alerted if an earlier slot appears


myTestDateString = 'Wednesday 12 June 2013 2:00pm'

myTestDate = datetime.strptime(myTestDateString, '%A %d %B %Y %I:%M%p')

# time to wait between each page request (set to a reasonable number
# to avoid hammering DSA's servers)
pauseTime = 5

def isBeforeMyTest(dt):
	if dt <= myTestDate:
		return True
	else:
		return False

def sendEmail(datetimeList):

	SMTPserver = 'smtp.gmail.com'
	sender =     'example@example.com'
	destination = ['example@example.com']

	USERNAME = "example@example.com"
	PASSWORD = "password"

	# typical values for text_subtype are plain, html, xml
	text_subtype = 'plain'

	content = "Available DSA test slots at Horsforth:\n\n"

	for dt in datetimeList:
		content += "* %s\n" % dt.strftime('%A %d %b %Y at %H:%M')

	content += "\nChecked at [%s]\n\n" % time.strftime('%Y-%m-%d @ %H:%M')

	subject="Driving Test Cancellations"

	import sys
	import os
	import re

	from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
	# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
	from email.MIMEText import MIMEText

	try:
	    msg = MIMEText(content, text_subtype)
	    msg['Subject']=       subject
	    msg['From']   = sender # some SMTP servers will do this automatically, not all

	    conn = SMTP(SMTPserver)
	    conn.set_debuglevel(False)
	    conn.login(USERNAME, PASSWORD)
	    try:
	        conn.sendmail(sender, destination, msg.as_string())
	    finally:
	        conn.close()

	except Exception, exc:
	    sys.exit( "mail failed; %s" % str(exc) ) # give a error message


def performUpdate():

	print '[%s]' % (time.strftime('%Y-%m-%d @ %H:%M'),)
	print '---> Starting update...'

	launcher = Page(launchPage, cookieJar)
	launcher.connect()
	launcher.acquireHiddenFields()
	launcher.fields['username'] = licenceNumber
	launcher.fields['password'] = theoryNumber
	
	# check to see if captcha
	captcha = launcher.html.find('div', id='recaptcha-check')
	if captcha:
		print 'Captcha was present, retry later'
		return
	print ''

	time.sleep(pauseTime)

	launcher.connect()
	if captcha:
		print launcher.html.find("Enter details below to access your booking")

	dateChangeURL = launcher.html.find(id="date-time-change").get('href')
	# example URL: href="/manage?execution=e1s1&amp;csrftoken=hIRXetGR5YAOdERH7aTLi14fHfOqnOgt&amp;_eventId=editTestDateTime"
	# i am probably screwing up the POST bit on the forms
	dateChangeURL = 'https://driverpracticaltest.direct.gov.uk' + dateChangeURL


	slotPickingPage = Page(dateChangeURL, cookieJar)
	slotPickingPage.fields = launcher.fields

	# slotPickingPage.acquireHiddenFields()
	slotPickingPage.connect()

	# should now be at the test centre search thing
	# slotPickingPage.acquireHiddenFields()

	e1s2URL = slotPickingPage.html.form.get('action')
	e1s2URL = 'https://driverpracticaltest.direct.gov.uk' + e1s2URL
	datePickerPage = Page(e1s2URL, cookieJar)

	datePickerPage.fields['testChoice'] = 'ASAP'
	datePickerPage.connect()

	# earliest available date

	availableDates = []

	for slot in datePickerPage.html(id="availability-results")[0].find_all('a'):
		if "Slot" in slot['id']:
			availableDates.append(datetime.strptime(slot.string.strip(), '%A %d %B %Y %I:%M%p'))


	print '---> Available slots:'
	
	soonerDates = []

	for dt in availableDates:
		if isBeforeMyTest(dt):
			print '-----> [CANCELLATION] %s' % (dt.strftime('%A %d %b %Y at %H:%M'),)
			soonerDates.append(dt)
		else:
			print '-----> %s' % (dt.strftime('%A %d %b %Y at %H:%M'),)
	
	if len(soonerDates):
		sendEmail(soonerDates)

performUpdate()

print ''

