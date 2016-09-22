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

from utils_selenium_authentication import Login, Cleaner
login = Login(debug=True, endpoint='companies')
browser = Cleaner(login.browser, debug=True)
tree = browser.tree

browser.findall("//div[@class='media-block__image']")

browser.close()
