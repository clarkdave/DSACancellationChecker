#!/usr/bin/python
"""

	DSA Checker
	For finding cancellations quickly and easily!
	
"""
import urllib, urllib2, cookielib, time, sys, os
from datetime import timedelta
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from DSACheckerClasses import Page, SlotsPage

# this should point at the DSA login page
launchPage = 'https://driverpracticaltest.direct.gov.uk/logincheck.aspx'

# the full licence number
licenceNumber = '*********'

# full theory certificate number
theoryNumber = '*********'

# date theory test was passed (on certificate)
theoryPassDate = ('2010', '01', '01')

# surname on driving licence
surname = 'Foo'

# birth date
birthDate = ('1990', '01', '01')

cookieJar = cookielib.CookieJar()

# these addresses will be mailed when a cancellation is found
emailAddresses = ['someone@example.com']
emailSubject = "DSA Cancellations"
emailFrom = "no-reply@example.com"

# test dates which are within this number of days will be considered
# as cancellations and will trigger an email
cancellationAlertDays = 20

# time to wait between each page request (set to a reasonable number
# to avoid hammering DSA's servers)
pauseTime = 5

def isCancellation(dt):
	# decide if this date is a cancellation based on
	# specific criteria

	# create timedelta
	delta = timedelta(days=cancellationAlertDays)
	
	threshold = datetime.today() + delta

	if dt <= threshold:
		return True
	else:
		return False

def sendEmail(datetimeList):
	p = os.popen('%s -t' % '/usr/sbin/sendmail', 'w')
	for address in emailAddresses:
		p.write("To: %s\n" % address)
	p.write("Subject: %s\n" % emailSubject)
	p.write("From: %s\n" % emailFrom)
	p.write("\n")

	# build email body

	content = "Available DSA test slots at Canterbury:\n\n"

	for dt in datetimeList:
		content += "* %s\n" % dt.strftime('%A %d %b %Y at %H:%M')

	content += "\nChecked at [%s]\n\n" % time.strftime('%Y-%m-%d @ %H:%M')

	p.write(content)
	status = p.close()
	
	if status:
		print '---> ! An error occured when sending emails'
	else:
		print '---> Sent emails to %s' % '; '.join(e for e in emailAddresses)


def performUpdate():

	print '[%s]' % (time.strftime('%Y-%m-%d @ %H:%M'),)
	print '---> Starting update...'

	launcher = Page(launchPage, cookieJar)
	launcher.connect()
	launcher.acquireHiddenFields()
	launcher.fields['txtLicence'] = licenceNumber
	launcher.fields['txtTheoryPass'] = theoryNumber
	launcher.fields['txtAppRefNo'] = ''
	launcher.fields['x'] = '35'
	launcher.fields['y'] = '17'
	
	# check to see if it's down...
	sorryCannot = launcher.html.find('span', id='SorryCannot')
	if sorryCannot:
		print "---> ! Booking system is down, exiting..."
		#sendEmail([])
		return
	
	time.sleep(pauseTime)
	
	overviewPage = Page(launchPage, cookieJar)
	overviewPage.fields = launcher.fields
	overviewPage.connect()
	overviewPage.acquireHiddenFields()
	overviewPage.fields['changeTestDetails'] = 'Check for different dates'
	
	time.sleep(pauseTime)
	
	preferredSlotPage = Page('https://driverpracticaltest.direct.gov.uk/bookingdetails.aspx', cookieJar)
	preferredSlotPage.fields = overviewPage.fields
	preferredSlotPage.connect()
	preferredSlotPage.acquireHiddenFields()
	preferredSlotPage.fields['NextButton.x'] = '36'
	preferredSlotPage.fields['NextButton.y'] = '11'
	preferredSlotPage.fields['PrefDate:Day1'] = 'dd'
	preferredSlotPage.fields['PrefDate:Month1'] = 'mm'
	preferredSlotPage.fields['PrefDate:Year1'] = 'yyyy'
	preferredSlotPage.fields['optWhen'] = '2'
	
	time.sleep(pauseTime)
	
	slotResultsPage = SlotsPage('https://driverpracticaltest.direct.gov.uk/slotpreferences.aspx', cookieJar)
	slotResultsPage.fields = preferredSlotPage.fields
	slotResultsPage.connect()
	datetimeList = slotResultsPage.acquireDateSlots()
	cancellationList = []
	
	print '---> Available slots:'
	
	for dt in datetimeList:
		if isCancellation(dt):
			cancellationList.append(dt)
			print '-----> [CANCELLATION] %s' % (dt.strftime('%A %d %b %Y at %H:%M'),)
		else:
			print '-----> %s' % (dt.strftime('%A %d %b %Y at %H:%M'),)
	
	#if len(cancellationList):
		#sendEmail(cancellationList)

performUpdate()

print ''

