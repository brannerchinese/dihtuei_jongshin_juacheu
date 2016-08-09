# main.py
# David Branner

import requests
import os
from lxml import html
from urllib.parse import urlunparse

import config

class Login():
    """Create and populate login object."""
    def __init__(self):
        self.credentials = None
        self.config = None
        self.session = None
        self.input_fields = None
        self.private = None

        # Populate attributes
        self.configure()
        self.create_session()
        self.log_in()

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
        root = html.document_fromstring(response.content)
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
        # returns /private
        self.private = self.session.post(url, data=self.input_fields)

    def fetch_all_paths(self):
        """Fetch all known paths."""
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
        print('\nRequested {}\nResponse code: {}'.format(url, r.status_code))
        return r

# works up to here.

