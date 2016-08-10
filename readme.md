# DSA Cancellation Checker

A small Python shell script which logs in to the DSA test checking website to look for cancellations. If it finds one, it will send an email to one or more addresses with the dates and times.

It will only work if you already have a booking, as this is generally the case when you look for a cancellation (you book a test in the future, and check regularly to see if you can get it moved forward). With a bit more work, this script could be updated to actually book the cancellation for you, as you don't need to re-enter payment details if you are simply changing your slot.

**Last confirmed working:** August 2016

## Usage

First, open up "DSAChecker.py" and fill in the fields with your details.

The Gmail username and password is required to send you cancellation notification emails, and is only ever used to authenticate with Gmail's servers to allow the script to send emails.

To run on Windows, simply create a scheduled task, running DSAChecker.py at your desired interval.

On Unix-like systems, you can use a cron job:

	*/15 6-23 * * * /app/dsa/DSAChecker.py >> /app/dsa/check.log 2>&1
	
The above will run the script every 15 minutes between the hours of 6am and 11pm. The DSA website is currently taken offline outside of these hours - if this is no longer the case, you could just run it all day.

## Requirements

* For obvious reasons, you can only use this if you are actually looking to book a test
	* Specifically, you need a valid application number for your existing booking and provisional licence
* A Gmail account to send emails via SMTP (however, modifying the script to use an alternative email provider is trivial). If you send via Gmail you'll need to accept access for less secure apps in your Google settings.
* Python 2.7
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

## Limitations

If you repeatedly run the script, the DSA website will start serving you up captchas. They are solvable by computers, but this requires use of a paid service (companies that sell software to check for DSA cancellations utilize these).

At some point in the future I may include something to prompt you to solve the captcha.

## Long term support

It's not possible to test this script without a 'guinea pig' who is currently looking to book a test. For this reason, the script may no longer function (DSA occasionally change their pages which will unavoidably break this script). However, it is quite easy to amend the script to accommodate any changes and I encourage people to do so.

Every now and then a friend of mine who is looking to book a cancellation will let me use their details to update the script, so I may periodically update the source to work with the latest version of the website.

## License 

Modifications for new gov.uk website (c) 2013 Josh Palmer (joshpalmer123@gmail.com)

Original Version copyright (c) 2010-2011 Dave Clark (contact@clarkdave.net)

(The MIT License)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
