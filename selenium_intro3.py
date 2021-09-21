"""
Exercise:
- Understanding what a URL is made up of, and what are query parameters
- Get list of past pycon events
- Get the duration, details, and location into a csv file
"""

import os
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode

# Getting webdriver
browser = webdriver.Chrome(ChromeDriverManager().install())

# Going directly to the url with query parameters
query_params = [
    ('q', 'pycon'),
]

encoded_params = urlencode(query_params)
print(encoded_params)
browser.get(f'http://www.python.org/search/?{encoded_params}')

# Get list of recent events
recent_events = browser.find_element_by_class_name('list-recent-events')
events = recent_events.find_elements_by_css_selector('li')
event_details = []
headers = ['Duration', 'Location', 'Description']

# There are past events and current events. Get only the past events
for event in events:
    if 'Event' in event.find_element_by_css_selector('h3').text:
        tmp_event_details = {
            'name': event.find_element_by_css_selector('h3 a').text
        }

        # The details are each in event are in <p>
        details = event.find_elements_by_css_selector('p')

        for index, detail in enumerate(details):
            tmp_event_details[headers[index]] = detail.text

        event_details.append(tmp_event_details)

print(event_details)
browser.quit()

# Put details in a dataframe
df = pd.DataFrame(event_details)
print(df)

# Save it into a csv file
df.to_csv(f'{os.path.dirname(__file__)}/python_events.csv', index=False)
