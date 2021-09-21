"""
Webscraper for property guru
"""

import os
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode

# Getting webdriver
browser = webdriver.Chrome(ChromeDriverManager().install())

# Getting filter properties
# Observer what happens when you search something
query_params = [
    ('minsize', 470),
    ('maxprice', 2500),
    ('market', 'residential'),
    ('beds[]', 1),
]

# Circle line from Serangoon to HarbourFront
for i in range(13, 29):
    query_params.append(('MRT_STATIONS[]', f'CC{i}'))

# Green line from Tanjong Pagar to Jurong East
for i in range(15, 24):
    query_params.append(('MRT_STATIONS[]', f'EW{i}'))

# Put all search filters in the url
encoded_params = urlencode(query_params)
browser.get(
    f'https://www.propertyguru.com.sg/property-for-rent?{encoded_params}'
)

properties = []

while True:
    element = browser.find_elements_by_class_name('listing-card')

    for elem in element:
        property_details = {
            'Name': elem.find_element_by_css_selector('h3 a').text,
            'Address': elem.find_element_by_css_selector(
                '.listing-location'
            ).text,
            'Price': elem.find_element_by_css_selector('.price').text,
            'Floor Area': elem.find_element_by_css_selector(
                '.listing-floorarea'
            ).text,
            'Distance': elem.find_element_by_css_selector(
                'ul[data-automation-id=listing-features-walk] li'
            ).text,
            'Link': elem.find_element_by_css_selector('h3 a').get_attribute(
                'href'
            ),
        }
        try:
            property_details[
                'Availability'
            ] = elem.find_element_by_css_selector('.listing-availability').text
        except:
            continue
        finally:
            properties.append(property_details)

    try:
        # If next page is disabled, we are on the last page
        next_page = browser.find_element_by_css_selector(
            '.pagination-next.disabled'
        )
        break
    except:
        # Not on the last page, go to next page
        next_page = browser.find_element_by_css_selector('.pagination-next')
        next_page_url = next_page.find_element_by_css_selector(
            'a'
        ).get_attribute('href')

        # Property guru detects that we are a bot when redirecting
        # To counter this, we open use a new driver for each page
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(next_page_url)

browser.quit()
df = pd.DataFrame(properties)
df.to_csv(f'{os.path.dirname(__file__)}/properties.csv', index=False)
