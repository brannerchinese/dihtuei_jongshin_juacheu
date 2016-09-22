## PhantomJS

 1. Install `phantomjs` binary. 
 
    * [Download](http://phantomjs.org/download.html) the package and copy the binary `bin/phantomjs` into current project directory.
    * The path of this binary is passed to `webdriver.PhantomJS`, so if the binary is placed elsewhere, the code must reflect that.

 1. Sample code derived from [Techstonia blog](http://techstonia.com/scraping-with-phantomjs-and-python.html):
 
    ```python
    from bs4 import BeautifulSoup
    from selenium import webdriver
    
    PHANTOMJS_PATH = './phantomjs'
    
    browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    
    # Test a dynamic site
    browser.get(
            '''http://www.scoreboard.com/en/tennis/atp-singles/'''
            '''us-open-2015/results/''')
    soup = BeautifulSoup(browser.page_source, "html.parser")
    games = soup.find_all('tr', {'class': 'stage-finished'})
    print(games[0].prettify())
    
    # Test Google's home page, standard test
    browser.get('https://google.com')
    print(browser.title)
    ```
    
    Both tests work correctly and no visible browser opens. Tried code `companies_selenium_authentication_manual.py`.
    
 1. However, React does not seem to run with PhantomJS (there are complaints about that around the web). Juriy Zaytsev maintains compatibility tables for [ES5](http://kangax.github.io/compat-table/es5/) and [ES6](http://kangax.github.io/compat-table/es6/); the former currently (20160920) shows two features of ES5 that PhantomJS and WebKit do not support. 
    
    Next try should be to use a regular browser.

### Libraries for PhantomJS

See `[phantompy](https://github.com/niwinz/phantompy) (docs herehttps://phantompy.readthedocs.io/en/latest/)`. (Not explored.)

[end]