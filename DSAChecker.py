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
licenceNumber = '******'

# full theory certificate number
theoryNumber = '*****'

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


myTestDateString = 'Thursday 4 July 2013 2:00pm'

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
	print 'Not implemented yet on windows'
	return;

	# p = os.popen('%s -t' % '/usr/sbin/sendmail', 'w')
	# for address in emailAddresses:
	# 	p.write("To: %s\n" % address)
	# p.write("Subject: %s\n" % emailSubject)
	# p.write("From: %s\n" % emailFrom)
	# p.write("\n")

	# # build email body

	# content = "Available DSA test slots at Horsforth:\n\n"

	# for dt in datetimeList:
	# 	content += "* %s\n" % dt.strftime('%A %d %b %Y at %H:%M')

	# content += "\nChecked at [%s]\n\n" % time.strftime('%Y-%m-%d @ %H:%M')

	# p.write(content)
	# status = p.close()
	
	# if status:
	# 	print '---> ! An error occured when sending emails'
	# else:
	# 	print '---> Sent emails to %s' % '; '.join(e for e in emailAddresses)


def performUpdate():

	print '[%s]' % (time.strftime('%Y-%m-%d @ %H:%M'),)
	print '---> Starting update...'

	launcher = Page(launchPage, cookieJar)
	launcher.connect()
	launcher.acquireHiddenFields()
	launcher.fields['driving-licence-number'] = licenceNumber
	launcher.fields['application-reference-number'] = theoryNumber
	
	# check to see if captcha
	captcha = launcher.html.find('div', id='recaptcha-check')
	if captcha:
		print 'Captcha was present, stop DOSing gov.uk idiot'
		return

	print ''

	time.sleep(pauseTime)

	launcher.connect()

	dateChangeURL = launcher.html.find(id="date-time-change").get('href')
	# example URL: href="/manage?execution=e1s1&amp;csrftoken=hIRXetGR5YAOdERH7aTLi14fHfOqnOgt&amp;_eventId=editTestDateTime"
	# i am probably screwing up the POST bit on the forms
	dateChangeURL = 'https://driverpracticaltest.direct.gov.uk' + dateChangeURL


	slotPickingPage = Page(dateChangeURL, cookieJar)
	slotPickingPage.fields = launcher.fields

	slotPickingPage.acquireHiddenFields()
	slotPickingPage.connect()

	# should now be at the test centre search thing
	slotPickingPage.acquireHiddenFields()
	slotPickingPage.connect()

	# earliest available date

	availableDates = []

	for slot in slotPickingPage.html(id="availability-results").find_all('a'):
		availableDates.append(datetime.strptime(slot.string, '%A %d %B %Y %I:%M%p'))


	print '---> Available slots:'
	
	for dt in availableDates:
		if isBeforeMyTest(dt):
			print '-----> [CANCELLATION] %s' % (dt.strftime('%A %d %b %Y at %H:%M'),)
		else:
			print '-----> %s' % (dt.strftime('%A %d %b %Y at %H:%M'),)
	
	#if len(cancellationList):
		#sendEmail(cancellationList)

performUpdate()

print ''

