from bs4 import BeautifulSoup
from selenium import webdriver

PHANTOMJS_PATH = './phantomjs'

browser = webdriver.PhantomJS(PHANTOMJS_PATH)

# Test a dynamic site
browser.get('http://www.scoreboard.com/en/tennis/atp-singles/us-open-2015/results/')
soup = BeautifulSoup(browser.page_source, "html.parser")
games = soup.find_all('tr', {'class': 'stage-finished'})
print(games[0].prettify())

# Test Google's home page, standard test
browser.get('https://google.com')
print(browser.title)