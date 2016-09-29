from pyvirtualdisplay import Display
from selenium import webdriver

with Display(visible=0, size=(800, 600)) as xvfb:
    browser = webdriver.Chrome()
    browser.get('http://www.google.com')
    print(browser.title)
    browser.quit()
