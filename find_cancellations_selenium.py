#!/usr/bin/python3
#for webdriver + interactions
from selenium import webdriver
#for explicit wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#to download and display image
import urllib.request
from PIL import Image 
import os
#for date manipulation
from datetime import datetime

from info import licenceNumber as DR_LIC_NUM
from info import theoryNumber as APP_REF_NUM 
from info import myTestDateString as CURRENT_TEST_TEXT
CURRENT_TEST_DATETIME = datetime.strptime(CURRENT_TEST_TEXT, "%A %d %B %Y %I:%M%p")
Path_chromedriver="/usr/lib/chromium-browser/chromedriver" #for linux

#request user solution
#error checking?
def get_user_captcha_sol():
	sol = None
	while not sol:
		sol = input('Type Catcha Solution: ')
		if not sol:
			print('Input is blank')
	return sol

#download captcha image from src, open the image and request user solution
#delete captcha image and return user sol
def display_captcha_image_and_get_sol(captcha_image_elems):
	input()
	captcha_image = captcha_image_elems
	captcha_image_src = captcha_image.get_attribute('src')
	urllib.request.urlretrieve(captcha_image_src, 'local_captcha_image')
	image = Image.open('local_captcha_image')
	image.show()
	captcha_input = get_user_captcha_sol()
	image.close()
	os.remove('local_captcha_image')
	return captcha_input

#look for captcha
#if it's there, input user solution and return true
#if not there, return false
def deal_with_captcha(driver):
	#driver.implicitly_wait(4)
	try:
		wait = WebDriverWait(driver, 2)
		captcha_image_elems = wait.until(EC.presence_of_element_located((By.ID,'recaptcha_challenge_image')))
		#captcha_image_elems = driver.find_elements_by_id("recaptcha_challenge_image")
	#if len(captcha_image_elems) > 0:
		captcha_input = display_captcha_image_and_get_sol(captcha_image_elems)
		captcha_response_field = driver.find_element_by_name('recaptcha_response_field')
		captcha_response_field.send_keys(captcha_input)
		captcha_response_field.submit()
		return True
	except TimeoutException:
	#else:
		return False

#navigates to list of earliest available tests in Selenium element format using selenium Chrome webdriver
#dealing with captchas if they arise
def extract_raw_HTML_tag_list():
	#open browser
	driver = webdriver.Chrome(Path_chromedriver)

	#go to landing page, find button to next page and click
	landing_page = driver.get("https://www.gov.uk/change-driving-test")
	link = driver.find_element_by_link_text('Start now')
	link.click()

	#fill out form, check if captcha, submit if deal_with_captcha didn't already submit
	username_box = driver.find_element_by_name('username')
	username_box.send_keys(DR_LIC_NUM)

	password_box = driver.find_element_by_name('password')
	password_box.send_keys(APP_REF_NUM)
	if not deal_with_captcha(driver):
		continue_btn = 	driver.find_element_by_name('booking-login')
		continue_btn.click()

	#find and click change button
	change_button = driver.find_element_by_id('date-time-change')
	change_button.click()

	#go to third page and check the box to get earliest available tests, submit
	radio_btn = driver.find_element_by_id('test-choice-earliest')
	radio_btn.click()
	radio_btn.submit()
	deal_with_captcha(driver)

	#list of earliest available tests
	button_board = driver.find_element_by_class_name('button-board')
	a_list = button_board.find_elements_by_xpath(".//a")
	return a_list

#converts each the text of each HTML tag in a_list to datime object in date_time_list
def convert_HTML_to_datetime(a_list):
	date_time_list = []
	for tag in a_list:
		tag_text = tag.text.strip()
		tag_datetime =  datetime.strptime(tag_text, "%A %d %B %Y %I:%M%p")
		date_time_list.append(tag_datetime)
	return date_time_list

#returns all earliest available tests in datetime format from website
def find_earliest_available_tests():
	a_list = extract_raw_HTML_tag_list()
	date_time_list = convert_HTML_to_datetime(a_list)
	return date_time_list

#filters datetimelist to only those tests before CURRENT_TEST_DATETIME
#then prints out each string in the filtered test list
def list_pre_curr_tests(date_time_list):
	pre_curr_list = []

	for test_datetime in date_time_list:
		if test_datetime < CURRENT_TEST_DATETIME:
			test_date_str = datetime.strftime(test_datetime, "%A %d %B %Y %I:%M%p")
			pre_curr_list.append(test_date_str)

	if pre_curr_list:
		for test_str in pre_curr_list:
			print(test_str)
		input('Press enter to quit')

#find earliest available tests from websites, then lists all tests before CURRENT_TEST_DATETIME
def open_web():
	date_time_list = find_earliest_available_tests()
	list_pre_curr_tests(date_time_list)

if __name__ == "__main__":
    date_time_list = find_earliest_available_tests()
    list_pre_curr_tests(date_time_list)
