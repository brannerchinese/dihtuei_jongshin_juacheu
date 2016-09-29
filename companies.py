#!/usr/bin/python
# companies.py
# David Branner

import datetime
import hashlib
import html
import json
import lxml
import os
import re

from utils import Login

def get_all_companies(path='companies'):
    """Collect list of companies and check if changed since last time."""
    # Get all companies.
    print('\nInitiating log-in to site... ', end='', flush=True)
    login = Login()
    print('complete.\nCleaning response... ', end='', flush=True)
    login.find_root_and_text(path)
    print('complete.')

    # Company names are present but apparently not in HTML;
    # so recover using regex instead of LXML.
    pattern = re.compile("""(?<=&quot;,&quot;name&quot;:&quot;)
                            (.{1,40}?)           # Company name <= 40 chars.
                            (?=&quot;,&quot;logo_url)""",
                            re.VERBOSE)
    return pattern.findall(login.html)

def report(date, old, new):
    """Report date and differences between sets "old" and "new"."""
    added = sorted(list(new-old))
    added = '\n * '.join(added)
    if added:
        print('\nCompanies added since {}: \n\n * {}'.format(date, added))
    removed = sorted(list(old-new))
    removed = '\n * '.join(removed)
    if removed:
        print('\nCompanies removed since {}: \n\n * {}'.format(date, removed))

def update_companies(path='companies'):
    """Find current companies; check against saved list; update if needed."""
    companies = get_all_companies(path)
    # Normalize HTML entities => ASCII.
    companies = [html.unescape(item) for item in companies]

    # Check against saved record.
    dir = 'last_saved_data'
    json_file = os.path.join(dir, path + '.json')

    # Create directory if it doesn't exist; read file if it does exist.
    if not os.path.exists(dir):
        os.makedirs(dir)
        print('\nNo directory *{} found; new directory created.'.format(dir))
    if os.path.exists(json_file):
        print('\n{}\n'.format(json_file))
        with open(json_file, 'r') as f:
            old_json = json.load(f)
    else:
        old_json = set()
        with open(json_file, 'w') as f:
            f.write('')
            print('\nNo file *{} found; empty file created.'.format(json_file))
    
    # Get old_date, get old_companies or set to empties.
    date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%S')
    if old_json:
        old_date = old_json['date']
        old_companies = set(old_json['companies'])
        report(date=old_date, old=old_companies, new=set(companies))
    else:
        old_date = '(no date)'
        old_companies = set()

    # Report and write new data.
    if old_companies != set(companies):
        payload = {'date': date, 'companies': companies}
        with open(json_file, 'w') as f:
            f.write(json.dumps(payload))
        print('\nUpdated data saved to: "{}",\n * date: {}\n * items: {}.\n'.
                format(json_file, date, len(companies)))
    else:
        print('\nNo change found in list of companies since {}.\n'.
                format(old_date))

if __name__ == '__main__':
    update_companies()