#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 22:15:47 2022

@author: jasonlcyy
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py

# chart studio setup
username = 'Jasonlcyy'
api_key = 'M7tIXqtBJct4PZMO6cQJ'
chart_studio.tools.set_credentials_file(username=username,
                                        api_key=api_key)

# disable google popup notifications to avoid web scraping being obstructed
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")

# selenium setup for web scraping
driver_path = "/Users/jasonlcyy/Downloads/chromedriver"
browser = webdriver.Chrome(executable_path = driver_path, chrome_options = chrome_options)

# website format
hkta = "https://www.hkta.edu.hk/en/jobcase{}"

# empty list to store listings
cases = []

# 2 different websites of listings
for j in ['', '2']:
    # go to the website
    browser.get(hkta.format(j))
    # iterate through all 167 pages
    for count in range(167):
        try:
            # wait for popup window and close it
            wait = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[3]/div/div/div[1]/div[3]/button/span/i')))
            wait.click()
        except:
            pass
        # scroll the page to load listings that are not available yet
        for scroll in range(3):
            # interval between scrolling to prevent page spilling over and affect the web scraping
            time.sleep(3)
            # script for scrolling the inner window
            browser.execute_script('document.querySelector("#main > div.v-application--wrap > div:nth-child(1) > section > div > div").scrollTop=20000')
        for i in range(1, 101):
            try:
                # locate the case number and the info regarding the level of the student
                case_number = browser.find_element('xpath', '//*[@id="main"]/div[1]/div[1]/section/div/div/div[2]/div[4]/div[{}]/div/button/div[1]/div[1]/div/div/p[1]'.format(str(i)))
                info = browser.find_element('xpath', '//*[@id="main"]/div[1]/div[1]/section/div/div/div[2]/div[4]/div[{}]/div/button/div[1]/div[1]/div/div/p[2]'.format(str(i)))
                # append pairs of case numbers and listing info
                cases.append([case_number.text, info.text])
            except NoSuchElementException:
                break
        try:
            # if all cases of that page are scraped, wait for the next page button to load and click it to go to the next page
            button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div[1]/section/div/div/div[2]/div[5]/div/ul/li[11]/button')))
            button.click()
        except:
            break

browser.quit()

case_no = []

level = []

for case in cases:
    # slice the case number to having the id only
    case_no.append(case[0][9:])
    # split the text to acquire the level of the student
    level.append(case[1].split(',')[0])

# construct dataframe for plotly output
all_cases = pd.DataFrame({'Case number': case_no, 'Level': level})

# only keep the relevant level, which are all in the dictionary below
# declare the equivalent age of that level for mapping later
keep = {'K1': 4, 'K2': 5, 'K3': 6, 'Primary 1': 7, 'Primary 2': 8, 'Primary 3': 9, 'Primary 4': 10, 'Primary 5': 11, 'Primary 6': 12
        , 'Form 1': 13, 'Form 2': 14, 'Form 3': 15, 'Form 4': 16, 'Form 5': 17, 'Form 6': 18}

# group by level and attain the total number of listings of respective levels
level_summary = all_cases.groupby(by = 'Level').size().sort_values(ascending = False).reset_index()

# only keep the desired text for levels
output = level_summary[level_summary['Level'].isin(keep.keys())]

# map the age from the dictionary
output['Age'] = output['Level'].apply(lambda x: keep[x])

''' read csv '''
# output = pd.read_csv('/Users/jasonlcyy/Desktop/HK Project/HKTA.csv').set_index('Unnamed: 0')

# rename the column for easier accessibility
output.rename(columns = {'0': "Number of cases"}, inplace = True)

# sort values by age
output = output.sort_values(by = 'Age')

output.reset_index(drop = True, inplace = True)

# declare plotly figure
tutoring = go.Figure()

# add kindergarten level bars
tutoring.add_trace(go.Bar(x = output['Age'].iloc[0:3], y = output['Number of cases'].iloc[0:3],
                          marker_color = '#ffcc99',
                          name = 'Kindergarten', xaxis = 'x2'))

# add primary level bars
tutoring.add_trace(go.Bar(x = output['Age'].iloc[3:9], y = output['Number of cases'].iloc[3:9],
                          marker_color = '#ffb3b3',
                          name = 'Primary School', xaxis = 'x2'))

# add secondary level bars
tutoring.add_trace(go.Bar(x = output['Age'].iloc[9:], y = output['Number of cases'].iloc[9:],
                          marker_color = '#9999ff',
                          name = 'Secondary School', xaxis = 'x2'))

# add dummy bar to generate secondary x axis
tutoring.add_trace(go.Bar(x = output['Level'], y = output['Number of cases'],
                          marker_color = 'white',
                          xaxis = 'x',
                          name = '',
                          showlegend = False))

# update layout to improve the readability of data visualization
tutoring.update_layout(title = 'Active Tutoring Listings<br><sup>Gaining a Headstart</sup>',
                       titlefont = dict(size = 28,
                                        family = 'Trajan'),
                       xaxis = dict(title = '', 
                                    tickmode = 'linear',
                                    tickfont = dict(size = 14,
                                                    family = 'Trajan'),
                                    side = 'top',
                                    domain = [0.01, 1]),
                       xaxis2 = dict(title = 'Equivalent Age',
                                     tickmode = 'linear',
                                     overlaying = 'x',
                                     tickfont = dict(size = 14,
                                                     family = 'Trajan'),
                                     titlefont = dict(size = 18,
                                                      family = 'Trajan'),
                                     side = 'bottom',
                                     domain = [0.01, 1]),
                       yaxis = dict(title = 'Number of Listings',
                                    tickfont = dict(size = 14,
                                                    family = 'Trajan'),
                                    titlefont = dict(size = 18,
                                                     family = 'Trajan')),
                       bargap = 0.15,
                       legend = dict(
                           x = 0.02,
                           y = 0.98,
                           bgcolor = 'rgba(255, 255, 255, 0)',
                           bordercolor = 'rgba(255, 255, 255, 0)',
                           font = dict(size = 15,
                                       family = 'Trajan')))

# source as footnote
tutoring_note = 'Source:<a href="https://www.hkta.edu.hk/en/jobcase">Hong Kong Tutor Association</a>'

tutoring.add_annotation(
    showarrow=False,
    text=tutoring_note,
    font=dict(size=13,
              family = 'Trajan'), 
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.2
    )

py.plot(tutoring, filename = 'Tutoring', auto_open = True)

tutoring.show()
