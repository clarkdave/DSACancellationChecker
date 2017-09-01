
# DSA Cancellation Checker

A small Python shell script which logs in to the DSA test checking website to look for cancellations. If it finds one, it will send an email to one or more addresses with the dates and times.

It will only work if you already have a booking, as this is generally the case when you look for a cancellation (you book a test in the future, and check regularly to see if you can get it moved forward). With a bit more work, this script could be updated to actually book the cancellation for you, as you don't need to re-enter payment details if you are simply changing your slot.

**Last confirmed working:** 16 August 2017

## Usage

First, open up "info.py" and fill in the fields with your details.

Then, just run 'DSAChecker.py' using Python3

If you are using this version, do not use a cron job / scheduled task as this is performed within the script.

Users also can choose to send an email or open the web (inspired by github.com/bsthowell/find_cancellations) by setting action_choosen.

1) action_choosen = 0: Sending an email is chosen, the Gmail username and password is required in info.py to send you cancellation notification emails, and is only ever used to authenticate with Gmail's servers to allow the script to send emails.

2) action_choosen = 1: If user wants to open the web directly, this version provides the open_web() function which can open a browser immediately when an earlier date is found. I fount it is very useful espeically when you want to change your appointment. 
   make sure you have install chromedriver in /usr/lib/chromium-browser/chromedriver 

Users can open the DSA website directly by:

python find_cancellations_selenium.py

## Requirements

* For obvious reasons, you can only use this if you are actually looking to book a test
	* Specifically, you need a valid application number for your existing booking and provisional licence
* A Gmail account to send emails via SMTP (however, modifying the script to use an alternative email provider is trivial). If you send via Gmail you'll need to accept access for less secure apps in your Google settings.
* [Python 3.6.0](https://www.python.org/downloads/release/python-360/)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

You could install by:

pip install -r requirements.txt

* Remember to install this using python3

## Limitations

If you repeatedly run the script, the DSA website will start serving you up captchas. They are solvable by computers, but this requires use of a paid service (companies that sell software to check for DSA cancellations utilize these).

At some point in the future I may include something to prompt you to solve the captcha.

## Long term support

It's not possible to test this script without a 'guinea pig' who is currently looking to book a test. For this reason, the script may no longer function (DSA occasionally change their pages which will unavoidably break this script). However, it is quite easy to amend the script to accommodate any changes and I encourage people to do so.

Every now and then a friend of mine who is looking to book a cancellation will let me use their details to update the script, so I may periodically update the source to work with the latest version of the website.

## License

Migrate to Python 3 and modifications to work with updated site (c) 2017 Calvin Hobbes (goodoldme42@gmail.com)

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
