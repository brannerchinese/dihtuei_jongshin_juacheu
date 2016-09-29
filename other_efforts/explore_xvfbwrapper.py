from selenium import webdriver
from xvfbwrapper import Xvfb

with Xvfb() as xvfb:
    browser = webdriver.Chrome()
    browser.get('http://www.google.com')
    print(browser.title)
    browser.quit()
