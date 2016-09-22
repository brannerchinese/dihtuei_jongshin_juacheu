"""
import io
import lxml
import lxml.html
from selenium import webdriver

browser = webdriver.Chrome()
# Get login page.
url = 'https://www.recurse.com/login'
browser.get(url)

# Log in and receive /private
e = 'dpb@brannerchinese.com'
p = '70977097709770977097'
email_form = browser.find_element_by_xpath("//input[@id='email']")
pw_form = browser.find_element_by_xpath("//input[@id='password']")
email_form.send_keys(e)
pw_form.send_keys(p)
browser.find_element_by_xpath("//input[@type='submit']").click()
browser.save_screenshot('private.png')

# Get companies page.
url_companies = 'https://www.recurse.com/companies'
browser.get(url_companies)
browser.save_screenshot('companies.png')

parser = lxml.etree.HTMLParser(
                recover=True,
                remove_comments=True, # important bec. of random-length comment
                no_network=True,
                remove_blank_text=True)
tree = lxml.etree.parse(io.StringIO(browser.page_source), parser)
undesirables = [
                '//script',
                "//meta[@name=\'csrf-token\']", # or just get rid of all meta?
                "//link[@rel=\'stylesheet\']",
                ]

for undesirable in undesirables:
    need_to_remove = any(item in tree.iter()
                    for item in tree.xpath(undesirable))
    if need_to_remove:
        print('\nAny {} elements present?'.
                format(undesirable), need_to_remove
             )
        for element in tree.xpath(undesirable):
            print(' * acting now on {}'.
                    format(element))
            element.getparent().remove(element)
        print('All {} elements now removed?'.
                format(undesirable),
                all(item not in tree.iter()
                        for item in tree.xpath(undesirable))
             )
"""

import datetime
import hashlib
import json
import lxml
import os
import re

from utils_selenium_chrome import Login, Cleaner

def get_all_companies(path='companies'):
    """Collect list of companies."""

    # Get all companies.
    print('\nInitiating log-in to site... ', end='', flush=True)
    login = Login(debug=True, endpoint='companies')
    print('complete.\nCleaning response... ', end='', flush=True)
    tree = Cleaner(login.browser.page_source, debug=True).tree
    print('complete.')
    login.browser.close() # In case of later error.

    # Extract company names from <img alt...> values.
    companies = tree.findall("//div[@class='media-block__image']/img")
    return [dict(item.items())['alt'] for item in companies]
    
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

    # Check against saved record.
    dir = 'last_saved_data'
    json_file = os.path.join(dir, path + '.json')

    # Create directory if it doesn't exist; read file if it does exist.
    if not os.path.exists(dir):
        os.makedirs(dir)
        print('\nNo directory *{} found; new directory created.'.format(dir))
    if os.path.exists(json_file):
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
