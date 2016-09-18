#!/usr/bin/python
# utils.py
# David Branner

import datetime
import io
import hashlib
import json
import lxml
import lxml.html
import os
import re
import requests

from urllib.parse import urlunparse

import config

class Login():
    """Create and populate login object."""
    def __init__(self, debug=False):
        self.config = None
        self.credentials = None
        if debug == True:
            self.debug = debug
            print('\nDebugging on.')
        else:
            self.debug = False
        self.html = None
        self.input_fields = None
        self.parser = None
        self.private = None
        self.session = None
        self.undesirables = [
                '//script',
                "//meta[@name=\'csrf-token\']", # or just get rid of all meta?
                "//link[@rel=\'stylesheet\']",
                ]

        # Populate attributes
        self.configure()
        self.create_session()
        self.log_in()
        self.make_parser()

    def configure(self):
        """Get config and credential data."""
        configurations = config.Configurations()
        self.credentials = configurations.credentials
        self.config = configurations.config

    def create_session(self):
        """Create Requests session for cookie persistence."""
        self.session = requests.Session()

    def log_in(self):
        """Get login page, find input fields, post login data."""

        # Get login page.
        url = urlunparse(
                (self.config['scheme'], self.config['base_url'],
                    self.config['paths']['login'],
                '', '', '')
                )
        response = self.session.get(url)        # r.status_code = 200

        # Find form's input fields and update with email and password.
        root = lxml.html.document_fromstring(response.content)
        form = root.body.forms[0]
        self.input_fields = {item.name: item.value for item in form
                                        if item.tag == 'input'}
        self.input_fields.update({'email': self.credentials['email'],
                             'password': self.credentials['password']})

        # Post log-in data; special endpoint /sessions is used for this.
        url = urlunparse(
                (self.config['scheme'], self.config['base_url'], 'sessions',
                '', '', '')
                )
        # Initial log-in returns /private endpoint.
        self.private = self.session.post(url, data=self.input_fields)

    def fetch_all_paths(self):
        """Fetch all paths listed in config.secret."""
        return [self.fetch_path(path) for path in self.config['paths']]

    def fetch_path(self, path):
        """Log into desired path"""
        url = urlunparse(
            (self.config['scheme'], self.config['base_url'],
                self.config['paths'][path],
            '', '', '')
            )
        # returns "path" endpoint; see r.text
        r = self.session.get(url, data=self.input_fields)
        self.debug_print('\nRequested {}\nResponse code: {}'.
                format(url, r.status_code))
        return r

    def make_parser(self):
        """Instantiate parser"""
        self.parser = lxml.etree.HTMLParser(
                recover=True,
                remove_comments=True, # important bec. of random-length comment
                no_network=True,
                remove_blank_text=True)

    def find_root_and_text(self, path):
        """Find root of HTML as session.text, then clean."""
        fetched = None
        while not fetched:
            fetched = self.fetch_path(path)
        self.html = fetched.text
        self.tree = lxml.etree.parse(io.StringIO(fetched.text), self.parser)
        
        # Clean
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
                     
    def debug_print(self, *content):
        """Print statement that only prints if self.debug is True."""
        if self.debug:
            print(*content)
