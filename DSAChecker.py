#!/usr/bin/python
"""

	DSA Checker
	For finding cancellations quickly and easily!
	
"""
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, http.cookiejar, time, sys, os
from datetime import timedelta
from datetime import datetime
from bs4 import BeautifulSoup
from DSACheckerClasses import Page

##################################################################
#                                                                #
# Update the following variables with your own personal details: #
#                                                                #
##################################################################


# Driving license number (Example: MORGA657054SM9IJ)
licenceNumber = '****************'

# Application reference number 
# (This number was given when you booked the test. It can be found on your confirmation email.)
theoryNumber = '********'

# Email sending details

# The email addresses you wish to send notifications to
emailAddresses = ['example@example.com', 'MySecondEmailAddress@example.com']

emailSubject = "DSA Cancellations"
emailFrom = "no-reply@example.com"

# Enter your gmail account details here so that the script can send emails
emailUsername = 'example@gmail.com'
emailPassword = 'mypassword' # the password to your "example@gmail.com" account

# Change this (at your own risk) if you don't use gmail (e.g. to hotmail/yahoo/etc smtp servers
emailSMTPserver = 'smtp.gmail.com'

# Put in your current test date in the format "Thursday 4 July 2013 2:00pm"; you will be alerted if an earlier slot appears

myTestDateString = 'Wednesday 12 June 2013 2:00pm'

##################################################################
#                                                                #
#              DO NOT MODIFY ANYTHING BELOW THIS LINE            #
#                                                                #
##################################################################




myTestDate = datetime.strptime(myTestDateString, '%A %d %B %Y %I:%M%p')

# time to wait between each page request (set to a reasonable number
# to avoid hammering DSA's servers)
pauseTime = 5

cookieJar = http.cookiejar.CookieJar()

def isBeforeMyTest(dt):
	if dt <= myTestDate:
		return True
	else:
		return False

def sendEmail(datetimeList):
	# i should probably point out i pinched this from stackoverflow or something
	SMTPserver = emailSMTPserver
	sender =     emailFrom
	destination = emailAddresses

	USERNAME = emailUsername
	PASSWORD = emailPassword

	# typical values for text_subtype are plain, html, xml
	text_subtype = 'plain'

	content = "Available DSA test slots at your selected test centre:\n\n"

	for dt in datetimeList:
		content += "* %s\n" % dt.strftime('%A %d %b %Y at %H:%M')

	content += "\nChecked at [%s]\n\n" % time.strftime('%d-%m-%Y @ %H:%M')

	subject = emailSubject

	import sys
	import os
	import re

	from smtplib import SMTP as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
	# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
	from email.mime.text import MIMEText

	try:
	    msg = MIMEText(content, text_subtype)
	    msg['Subject']=       subject
	    msg['From']   = sender # some SMTP servers will do this automatically, not all

	    conn = SMTP(SMTPserver, 587)
	    conn.set_debuglevel(False)
	    conn.ehlo()
	    conn.starttls()     # Use TLS

	    conn.login(USERNAME, PASSWORD)
	    try:
	        conn.sendmail(sender, destination, msg.as_string())
	    finally:
	        conn.close()

	except Exception as exc:
	    sys.exit( "mail failed; %s" % str(exc) ) # give a error message


def performUpdate():

	# this should point at the DSA login page
	launchPage = 'https://driverpracticaltest.direct.gov.uk/login'

	print('[%s]' % (time.strftime('%Y-%m-%d @ %H:%M'),))
	print('---> Starting update...')

	launcher = Page(launchPage, cookieJar)
	launcher.connect()
	launcher.fields['username'] = licenceNumber
	launcher.fields['password'] = theoryNumber
	
	# check to see if captcha
	captcha = launcher.html.find('div', id='recaptcha-check')
	if captcha:
		print('Captcha was present, retry later')
		# TODO: implement something to solve these or prompt you for them
		return
	print('')

	time.sleep(pauseTime)

	launcher.connect()
	if captcha:
		print(launcher.html.find("Enter details below to access your booking"))

	dateChangeURL = launcher.html.find(id="date-time-change").get('href')
	# example URL: href="/manage?execution=e1s1&amp;csrftoken=hIRXetGR5YAOdERH7aTLi14fHfOqnOgt&amp;_eventId=editTestDateTime"
	# i am probably screwing up the POST bit on the forms
	dateChangeURL = 'https://driverpracticaltest.direct.gov.uk' + dateChangeURL


	slotPickingPage = Page(dateChangeURL, cookieJar)
	slotPickingPage.fields = launcher.fields

	slotPickingPage.connect()

	e1s2URL = slotPickingPage.html.form.get('action')
	e1s2URL = 'https://driverpracticaltest.direct.gov.uk' + e1s2URL
	datePickerPage = Page(e1s2URL, cookieJar)

	datePickerPage.fields['testChoice'] = 'ASAP'
	datePickerPage.fields['drivingLicenceSubmit'] = 'Continue'
	datePickerPage.fields['csrftoken'] = dateChangeURL.split('=')[3]
	
	datePickerPage.connect()

	# earliest available date

	availableDates = []

	for slot in datePickerPage.html.find_all(class_='SlotPicker-slot'):
		try: 
			availableDates.append(datetime.strptime(slot['data-datetime-label'].strip(), '%A %d %B %Y %I:%M%p'))
		except Exception as ex:
			print("".join(traceback.format_exception(etype=type(ex),value=ex,tb=ex.__traceback__)))
	print ('---> Available slots:')
	
	soonerDates = []

	for dt in availableDates:
		if isBeforeMyTest(dt):
			print ('-----> [CANCELLATION] %s' % (dt.strftime('%A %d %b %Y at %H:%M'),))
			soonerDates.append(dt)
		else:
			print ('-----> %s' % (dt.strftime('%A %d %b %Y at %H:%M'),))	
	if len(soonerDates):
		sendEmail(soonerDates)

performUpdate()
print('')

