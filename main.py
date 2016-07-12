# main.py
# David Branner

import requests
import os
from lxml import html
from urllib.parse import urlunparse

import config

# Get config and credential data.
configurations = config.Configurations()
credentials = configurations.credentials
config = configurations.config

# Create Requests session for cookie persistence.
s = requests.Session()

# Get login page.
url = urlunparse(
        (config['scheme'], config['base_url'], config['paths']['login'],
        '', '', '')
        )
response = s.get(url)        # r.status_code = 200

# Find form input fields and update with email and password.
root = html.document_fromstring(response.content)
form = root.body.forms[0]
input_fields = {item.name: item.value for item in form if item.tag == 'input'}
input_fields.update({'email': credentials['email'],
                     'password': credentials['password']})

# Post log-in data; special endpoint /sessions is used for this.
url = urlunparse(
        (config['scheme'], config['base_url'], 'sessions',
        '', '', '')
        )
r = s.post(url, data=input_fields)     # returns /private

# Log into desired path
for path in config['paths']:
    url = urlunparse(
        (config['scheme'], config['base_url'], config['paths'][path],
        '', '', '')
        )
    r = s.get(url, data=input_fields)      # returns "path" endpoint; see r.text
    print('\n{}\n{}'.format(url, r.status_code))

# works up to here.

