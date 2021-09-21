"""
Selenium introduction 1:
- Understand simple CSS
- Learn how to get elements by different selectors
- Learn how to input values input input fields
- Learn how to use keyboard key presses
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Getting webdriver
browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get('http://www.python.org')
assert 'Python' in browser.title

# Searching for elements using different selectors
# Can try out one by one to see that they work
search_box = browser.find_element_by_name('q')
search_box = browser.find_element_by_id('id-search-field')
search_box = browser.find_element_by_xpath('//*[@id="id-search-field"]')
search_box = browser.find_element_by_class_name('search-field')
search_box = browser.find_element_by_css_selector('form fieldset input')

# Input values into textbox
search_box.send_keys('pycon')

# Clearing textbox
search_box.clear()

# Button clicks
search_box.send_keys('pycon')
submit_button = browser.find_element_by_id('submit')
submit_button.click()

# Keyboard shortcuts
search_box.send_keys('pycon', Keys.RETURN)
assert 'No results found.' not in browser.page_source

browser.quit()

