## Notes about other things to explore

   * **iframes**: ee http://stackoverflow.com/questions/37187068/unable-to-scrape-data-from-a-react-js-data-grid. 
   * The more serious question is how to do all this without opening a browser window. [This post](http://stackoverflow.com/a/28090850/621762) describe three options:
   
     * with a headless browser like `PhantomJS` or `ghost.py`
     * with a virtual display like `xvfb`
     * with a remote selenium server on some custom server like BrowserStack or Sauce Labs

     The first two of these are discussed in their own READMEs.

 * **XPath**
 
   * See lxml.de/1.3/parsing.html#parsing-html; http://lxml.de/1.3/xpathxslt.html. Deal with class="media-block__image" on companies page; this is not accessible through LXML.
   * Remember the use of the FirePath add-on for identifying XPath for DOM elements.
   * Mozilla's [XPath docs](https://developer.mozilla.org/en-US/docs/Web/XPath)

 * LXML tutorial urges use of root = etree.Element("root")

[end]