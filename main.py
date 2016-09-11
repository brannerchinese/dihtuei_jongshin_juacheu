# main.py
# David Branner

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
    def __init__(self, debug=True):
        self.config = None
        self.credentials = None
        if debug == True:
            self.debug = debug
            print('\nDebugging on.')
        self.elements_to_remove = [
                '//script',
                "//meta[@name=\'csrf-token\']", # or just get rid of all meta?
                "//link[@rel=\'stylesheet\']",
                ]
        self.html = None
        self.input_fields = None
        self.parser = None
        self.private = None
        self.session = None

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
        self.debug_print('\nRequested {}\nResponse code: {}'.
                format(url, r.status_code))
        return r

    def remove_random_length_comment(self, text):
        """Remove length-hiding random comment. 
        
        Unnecessary for self.root, with parser(remove_comments=true).
        But still has to be removed from self.html manually.
        """
        to_remove = re.compile(
                "\n*<!-- This is a random-length HTML comment: [a-z]+? -->")
        new_text = re.sub(to_remove, '', text)
        self.debug_print('\nLength-hiding random comment removed: {}.'.
                format(len(text)>len(new_text)))
        return new_text

    def make_parser(self):
        """Instantiate parser"""
        self.parser = lxml.etree.HTMLParser(
                recover=True,
                remove_comments=True,
                no_network=True,
                remove_blank_text=True)

    def find_root_and_text(self, path):
        """Find root of HTML as session.text, then clean."""
        fetched = self.fetch_path(path)
        if fetched:
            text = fetched.text
        self.html = self.remove_random_length_comment(text)
        self.root = lxml.etree.parse(io.StringIO(self.html), self.parser)
        
        # Clean
        before_removing = len(list(self.root.iter()))
        self.remove_undesirable_elements()
        after_removing = len(list(self.root.iter()))
        self.debug_print('\nRemoved {} elements'.
                format(before_removing-after_removing))

    def remove_undesirable_elements(self):
        """If an 'undesirable' element is in document, remove and report."""
        for undesirable in self.elements_to_remove:
            need_to_remove = any(item in self.root.iter()
                            for item in self.root.xpath(undesirable))
            if need_to_remove:
                self.debug_print('\nAny {} elements present?'.
                        format(undesirable), need_to_remove
                     )
                for element in self.root.xpath(undesirable):
                    self.debug_print(' * acting now on {}'.
                            format(element))
                    element.getparent().remove(element)
                self.debug_print('All {} elements now removed?'.
                        format(undesirable),
                        all(item not in self.root.iter()
                                for item in self.root.xpath(undesirable))
                     )
                     
    def debug_print(self, *content):
        if self.debug:
            print(*content)

def find_updates(path='manual'):
    """Get desired page; see if it has changed; if so, report and save."""
    hash_file = path + '.hash'
    json_file = path + '.json'
    login = Login()
    login.find_root_and_text(path)

    # Convert to list of strings and then to JSON.
    list_of_strings = lxml.etree.tostringlist(login.root)
    list_of_strings = [item.decode() for item in list_of_strings]
    list_of_strings = json.dumps(list_of_strings)

    # Save hash and, if changed, file.
    # First check if we have files, and if so whether has has changed.
    ### TODO: not yet finished here
    hashed = hashlib.sha512(list_of_strings.encode()).hexdigest()
    with open(hash_file, 'w') as f:
        f.write(hashed)
    with open(json_file, 'w') as f:
        f.write(list_of_strings)

"""
# Running manually:
import main ; login = main.Login() ; login.find_root_and_text('manual')
"""

# See lxml.de/1.3/parsing.html#parsing-html; http://lxml.de/1.3/xpathxslt.html

# TODO: deal with class="media-block__image" on companies page

# TODO: LXML tutorial urges use of root = etree.Element("root")
