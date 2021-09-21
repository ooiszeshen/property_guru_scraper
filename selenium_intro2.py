"""
Selenium introduction 2:
- Learn how to get list of elements
- Learn what is select and options and how to loop through them
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

# Getting webdriver
browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get('http://www.python.org')
browser.find_element_by_class_name('donate-button').click()

frequency = browser.find_element_by_id('frequency_unit')

# Loop through 'options' in 'Select'
# Notice that 'elements' here is plural
options = frequency.find_elements_by_tag_name("option")

# Selecting 'year' option
for option in options:
    print("Value is: %s" % option.get_attribute("value"))
    if option.get_attribute("value") == 'year':
        option.click()

# A better way of doing selects
select_frequency = Select(browser.find_element_by_id('frequency_unit'))
select_frequency.select_by_visible_text('year')
select_frequency.select_by_value('year')

browser.quit()

