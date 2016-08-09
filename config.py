# config.py
# David Branner

"""Handle configuration and credentials; we use JSON."""

import json
import os

class Configurations():
    def __init__(self):
        credentials_file = 'credentials.secret'
        config_file = 'config.secret'

        with open(credentials_file, 'r') as f:
            self.credentials = json.loads(f.read())

        with open(config_file, 'r') as f:
            self.config = json.loads(f.read())
    
