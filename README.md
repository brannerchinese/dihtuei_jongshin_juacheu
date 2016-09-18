## Have New RC Companies Been Posted Since I Last Looked?

 1. Using `credentials.sample` and `config.sample` as models, populate `credentials.secret` and `config.secret`. Be sure to include a value for the "companies" key that shows the endpoint where RC companies are listed. If you're not sure what the endpoint is, visit the RC companies page — it's the last element of the path there.
 1. Run from the command line as `python companies.py`. This program runs in Python 3.

### Discussion

Because of the use of frameworks, company names are present in the file received through a `requests.Session` request but apparently not in the DOM proper; so we currently recover them using regex on the file instead of using LXML on the DOM.

### To do

 * Explore use of `selenium.webdriver`, instead. See http://stackoverflow.com/questions/37187068/unable-to-scrape-data-from-a-react-js-data-grid.

 * For XPath, see lxml.de/1.3/parsing.html#parsing-html; http://lxml.de/1.3/xpathxslt.html. Deal with class="media-block__image" on companies page; this is not accessible through LXML.

 * LXML tutorial urges use of root = etree.Element("root")
 * Remember the use of the FirePath add-on for identifying XPath for DOM elements. See https://developer.mozilla.org/en-US/docs/Web/XPath for documentation.

[end]