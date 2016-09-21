## Have New RC Companies Been Posted Since I Last Looked?

 1. Using `credentials.sample` and `config.sample` as models, populate `credentials.secret` and `config.secret`. Be sure to include a value for the "companies" key that shows the endpoint where RC companies are listed. If you're not sure what the endpoint is, visit the RC companies page — it's the last element of the path there.
 1. Run from the command line as `python companies.py`. This program runs in Python 3.

### Discussion

Because of the use of frameworks, company names are present in the file received through a `requests.Session` request but apparently not in the DOM proper; so we currently recover them using regex on the file instead of using LXML on the DOM.

### To do

 * **Selenium**. 
 
   Simple test works:
   
   ```python
   from selenium import webdriver
   
   browser = webdriver.Chrome()
   browser.get('http://www.google.com')
   print(browser.title)
   browser.quit()
   ```

   although we haven't yet tried authentication on RC site.
 
   * **iframes**: ee http://stackoverflow.com/questions/37187068/unable-to-scrape-data-from-a-react-js-data-grid. 
   * The more serious question is how to do all this without opening a browser window. [This post](http://stackoverflow.com/a/28090850/621762) describe three options:
   
     * with a headless browser like [`ghost.py`](http://ghost-py.readthedocs.io/en/latest/) (`PhantomJS` no longer supports Python.)
     * with a virtual display like `xvfb`
     * with a remote selenium server on some custom server like BrowserStack or Sauce Labs

     These are discussed in their own READMEs.


 * ** X Virtual FrameBuffer (Xvfb)**

   `Xvfb` seem to be installed as part of X11 or XQuartz. It runs at the OS X command line now and has a man page.

   1. `xvfbwrapper`

      Attempting to run using `webdriver.Firefox()` fails. Running with `webdriver.Chrome` requires installing ChromeDriver (done with Homebrew). Then, using as context manager, following http://stackoverflow.com/a/6300672/621762, and running from command line as root:
      
      ```python
      from selenium import webdriver
      from xvfbwrapper import Xvfb
      
      with Xvfb() as xvfb:
          browser = webdriver.Chrome()
          browser.get('http://www.google.com')
          print(browser.title)
          browser.quit()
      ```

      runs correctly, although it does seem still to open the browser. See https://sites.google.com/a/chromium.org/chromedriver/getting-started on `chromedriver`.

   
   2. `pyvirtualdisplay`

      Same as with `xvfbwrapper`. Fails with `webdriver.Firefox()`, but works with `webdriver.Chrome`, run from command line as root, but still shows browser.

      ```bash
      pip install pyvirtualdisplay
      ```
      
      The sample code from http://stackoverflow.com/a/6300672/621762:
      
      ```python
      from pyvirtualdisplay import Display
      from selenium import webdriver
      
      display = Display(visible=0, size=(800, 600))
      display.start()
      browser = webdriver.Firefox()
      ```

      does not open Firefox invisibuly.


 * **Ghost.py**
 
   Requires `pyside`, which requires Python v. 3.4; we are now at v. 3.5, so avoiding this for now.
 
 * **XPath**
 
   * See lxml.de/1.3/parsing.html#parsing-html; http://lxml.de/1.3/xpathxslt.html. Deal with class="media-block__image" on companies page; this is not accessible through LXML.
   * Remember the use of the FirePath add-on for identifying XPath for DOM elements.
   * Mozilla's [XPath docs](https://developer.mozilla.org/en-US/docs/Web/XPath)

 * LXML tutorial urges use of root = etree.Element("root")

[end]