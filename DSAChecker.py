#!/usr/bin/python
"""

	DSA Checker
	For finding cancellations quickly and easily!
	
"""
from datetime import datetime

import http.cookiejar
import time
import random

from DSACheckerClasses import Page

##################################################################
#                                                                #
# Update the following variables with your own personal details  #
# in info.py                                                     #
#                                                                #
##################################################################

from info import licenceNumber, theoryNumber, myTestDateString

# Email sending details

from info import emailAddresses, emailUsername, emailPassword
from find_cancellations_selenium import open_web

emailSubject = "DSA Cancellations"
emailFrom = "no-reply@example.com"

# Change this (at your own risk) if you don't use gmail (e.g. to hotmail/yahoo/etc smtp servers
emailSMTPserver = 'smtp.gmail.com'

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
    sender = emailFrom
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

    from smtplib import SMTP as SMTP  # this invokes the secure SMTP protocol (port 465, uses SSL)
    # from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
    from email.mime.text import MIMEText

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender  # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver, 587)
        conn.set_debuglevel(False)
        conn.ehlo()
        conn.starttls()  # Use TLS

        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.close()

    except Exception as exc:
        sys.exit("mail failed; %s" % str(exc))  # give a error message


soonerDates = []
baseWaitTime = 600
userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
]


def performUpdate():
    global baseWaitTime
    global userAgents
    global soonerDates

    # this should point at the DSA login page
    launchPage = 'https://driverpracticaltest.direct.gov.uk/login'

    print('[%s]' % (time.strftime('%Y-%m-%d @ %H:%M'),))
    print('---> Starting update...')

    # use a random agent for each run through
    agent = userAgents[random.randint(0, len(userAgents) - 1)]
    print("---> Using agent " + agent)

    launcher = Page(launchPage, cookieJar)
    launcher.connect(agent)
    launcher.fields['username'] = licenceNumber
    launcher.fields['password'] = theoryNumber

    # check to see if captcha
    captcha = launcher.html.find('div', id='recaptcha-check')
    if captcha:
        # server is suspicious, back off a bit!
        baseWaitTime *= 2
        print('Captcha was present, increased baseline wait time to ' + str(baseWaitTime/60) + ' minutes')
        # TODO: implement something to solve these or prompt you for them
        return
    print('')

    time.sleep(pauseTime)

    launcher.connect(agent)
    if captcha:
        print(launcher.html.find("Enter details below to access your booking"))

    dateChangeURL = launcher.html.find(id="date-time-change").get('href')
    # example URL: href="/manage?execution=e1s1&amp;csrftoken=hIRXetGR5YAOdERH7aTLi14fHfOqnOgt&amp;_eventId=editTestDateTime"
    # i am probably screwing up the POST bit on the forms
    dateChangeURL = 'https://driverpracticaltest.direct.gov.uk' + dateChangeURL

    slotPickingPage = Page(dateChangeURL, cookieJar)
    slotPickingPage.fields = launcher.fields

    slotPickingPage.connect(agent)

    e1s2URL = slotPickingPage.html.form.get('action')
    e1s2URL = 'https://driverpracticaltest.direct.gov.uk' + e1s2URL
    datePickerPage = Page(e1s2URL, cookieJar)

    datePickerPage.fields['testChoice'] = 'ASAP'
    datePickerPage.fields['drivingLicenceSubmit'] = 'Continue'
    datePickerPage.fields['csrftoken'] = dateChangeURL.split('=')[3]

    datePickerPage.connect(agent)

    # earliest available date

    availableDates = []

    for slot in datePickerPage.html.find_all(class_='SlotPicker-slot'):
        try:
            availableDates.append(datetime.strptime(slot['data-datetime-label'].strip(), '%A %d %B %Y %I:%M%p'))
        except Exception as ex:
            print("".join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
    print ('---> Available slots:')

    newSoonerDates = []
    for dt in availableDates[0:10]:
        # only show / send new appointments
        if isBeforeMyTest(dt) and (dt not in soonerDates):
            print ('-----> [CANCELLATION] %s' % (dt.strftime('%A %d %b %Y at %H:%M'),))
            soonerDates.append(dt)
            newSoonerDates.append(dt)
        else:
            print ('-----> %s' % (dt.strftime('%A %d %b %Y at %H:%M'),))

    if len(newSoonerDates):
        print('---> Sending to ' + ', '.join(emailAddresses))
        #sendEmail(newSoonerDates)
        open_web()

    if baseWaitTime > 300:
        # decrease the baseline wait time as this was a success
        baseWaitTime = int(baseWaitTime / 2)

while True:
    print('***************************************')
    performUpdate()
    # wait for baseline + random time so its less robotic
    sleepTime = baseWaitTime + random.randint(60, 300)
    print('---> Waiting for ' + str(sleepTime / 60) + ' minutes...')
    time.sleep(int(sleepTime))
