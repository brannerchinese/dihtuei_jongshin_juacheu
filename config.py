# config.py
# David Branner

"""Handle configuration and credentials."""

import json

class Configurations():
    credentials_file = 'credentials.secret'
    
    def __init__(self):
        with open(credentials_file, 'r') as f:
            self.credentials = json.loads(f.read())
    
    def assign_credentials(self):
        self.email = self.credentials['email']
        self.password = self.credentials['password']
        self.base_url = self.credentials['base_url']
        self.paths = self.credentials['paths']
