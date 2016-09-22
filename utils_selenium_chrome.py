#!/usr/bin/python
# selenium_authentication.py
# David Branner

import io
import lxml
import lxml.html
import requests
from selenium import webdriver
from urllib.parse import urlunparse

import config

class Login():
    """Create and populate login object."""
    def __init__(self, debug=False, endpoint=''):
        self.browser = webdriver.Chrome()
        self.config = None
        self.credentials = None
        self.debug_print = DebugPrinter(debug=debug).debug_print
        if debug:
            print('\nDebugging on.')
        self.input_fields = None
        self.private = None
        self.session = None

        # Populate attributes
        self.configure()
        self.log_in()
        self.get_endpoint(endpoint)

    def configure(self):
        """Get config and credential data."""
        configurations = config.Configurations()
        self.credentials = configurations.credentials
        self.config = configurations.config

    def log_in(self):
        """Get login page, find input fields, post login data."""

        # Get login page.
        self.get_endpoint(endpoint=self.config['paths']['login'])

        # Post log-in data.
        email_form = self.browser.find_element_by_xpath("//input[@id='email']")
        pw_form = self.browser.find_element_by_xpath("//input[@id='password']")
        email_form.send_keys(self.credentials['email'])
        pw_form.send_keys(self.credentials['password'])

        # Initial log-in returns /private endpoint.
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

    def get_endpoint(self, endpoint=''):
        url = urlunparse(
                (self.config['scheme'], self.config['base_url'], endpoint,
                '', '', '')
                )
        self.browser.get(url)


class DebugPrinter():
    def __init__(self, debug=False):
        self.debug = debug

    def debug_print(self, *content):
        """Print statement that only prints if self.debug is True."""
        if self.debug:
            print(*content)


class Cleaner():

    # TODO: in this class, we only need browser.page_source, not browser

    def __init__(self, page_source, debug=False):
        self.page_source = page_source
        self.debug_print = DebugPrinter(debug=debug).debug_print
        self.parser = None
        self.tree = None
        self.undesirables = [
                '//script',
                "//meta[@name=\'csrf-token\']", # or just get rid of all meta?
                "//link[@rel=\'stylesheet\']",
                ]

        self.make_parser()
        self.find_root()
        self.remove_undesirable_elements()
    
    def find_root(self):
        """Find root of HTML as self.browser.page_source, then clean."""
        self.tree = lxml.etree.parse(
                io.StringIO(self.page_source), self.parser)

        # Clean.
        before_removing = len(list(self.tree.iter()))
        self.remove_undesirable_elements()
        after_removing = len(list(self.tree.iter()))
        self.debug_print('\nRemoved {} elements'.
                format(before_removing-after_removing))

    def remove_undesirable_elements(self):
        """If an 'undesirable' element is in document, remove and report."""
        for undesirable in self.undesirables:
            need_to_remove = any(item in self.tree.iter()
                            for item in self.tree.xpath(undesirable))
            if need_to_remove:
                self.debug_print('\nAny {} elements present?'.
                        format(undesirable), need_to_remove
                     )
                for element in self.tree.xpath(undesirable):
                    self.debug_print(' * acting now on {}'.
                            format(element))
                    element.getparent().remove(element)
                self.debug_print('All {} elements now removed?'.
                        format(undesirable),
                        all(item not in self.tree.iter()
                                for item in self.tree.xpath(undesirable))
                     )

    def make_parser(self):
        """Instantiate parser"""
        self.parser = lxml.etree.HTMLParser(
                recover=True,
                remove_comments=True, # important bec. of random-length comment
                no_network=True,
                remove_blank_text=True)

