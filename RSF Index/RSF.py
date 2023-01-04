#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 21:21:00 2022

@author: jasonlcyy
"""
from selenium import webdriver
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py

# chart studio setup
username = 'Jasonlcyy'
api_key = 'M7tIXqtBJct4PZMO6cQJ'
chart_studio.tools.set_credentials_file(username=username,
                                        api_key=api_key)

# setup selenium setup for web scraping
driver_path = "/Users/jasonlcyy/Downloads/chromedriver"
browser = webdriver.Chrome(executable_path = driver_path)

# website format for different years
rsf = "https://rsf.org/en/index?year={}"

# range of years available with the same methodology
years = np.arange(2013, 2023)

# dictionary to store data by year
yearly_rsf = {}

for year in years:
    # empty list for countries and their respective indices
    countries = []
    indices = []
    # go to the website of that year
    browser.get(rsf.format(str(year)))
    for row in range(1, 200):
        try:
            # wait for the table to load before scraping
            country = WebDriverWait(browser, 10).until(EC.presence_of_element_located(('xpath', '//*[@id="block-rsf-content"]/div/div[4]/div[1]/div[2]/div[3]/div[{}]/div[1]/span[3]'.format(str(row)))))
            index = browser.find_element('xpath', '//*[@id="block-rsf-content"]/div/div[4]/div[1]/div[2]/div[3]/div[{}]/div[1]/span[4]'.format(str(row)))
            # append country and its index to the list
            countries.append(country.text)
            indices.append(float(index.text))
        # if no more elements are available, quit the loop
        except:
            break
    # construct the dataframe and store in the dictionary
    temp_df = pd.DataFrame({'Country': countries, 'Index': indices})
    yearly_rsf[year] = temp_df

# quit browser after scraping
browser.quit()

hk_scores = []
china_scores = []
ranks = []
means = []

# extract the relevant data from the scraped data
for data in yearly_rsf.values():
    temp_hk_score = data[data['Country'] == 'Hong Kong']['Index'].values[0]
    temp_china_score = data[data['Country'] == 'China']['Index'].values[0]
    temp_index = data[data['Country'] == 'Hong Kong']['Index'].index[0] + 1
    temp_mean = data['Index'].mean()
    hk_scores.append(temp_hk_score)
    china_scores.append(temp_china_score)
    ranks.append(temp_index)
    means.append(temp_mean)

# construct the dataframe for generating data visualization
rsf_df = pd.DataFrame({'Year': years, 'Score (Hong Kong)': hk_scores, 'Score (China)': china_scores, 'Rank (Hong Kong)': ranks, 'Global mean score': means})

''' read csv '''
# rsf_df = pd.read_csv('/Users/jasonlcyy/Desktop/HK Project/RSF.csv').set_index('Unnamed: 0')

# declare plotly figure
fig = go.Figure()

# color list to specify colors for each column/bar
colors = ['#000066']*len(rsf_df.index)
colors[len(rsf_df.index)-1] = '#ffb3b3'

# add bar chart for Hong Kong Score
fig.add_trace(go.Bar(x = rsf_df['Year'], y = rsf_df['Score (Hong Kong)'], 
                     name = 'Hong Kong', yaxis = 'y',
                     marker_color=colors))

# add bar chart for global average
fig.add_trace(go.Bar(x = rsf_df['Year'], y = rsf_df['Global mean score'], 
                     name = 'Global Mean', yaxis = 'y',
                     marker_color = '#6666ff'))

# add bar chart for China Score
fig.add_trace(go.Bar(x = rsf_df['Year'], y = rsf_df['Score (China)'], 
                     name = 'China', yaxis = 'y',
                     marker_color = '#9999ff'))

# add line chart for Hong Kong Rank
fig.add_trace(go.Scatter(x = rsf_df['Year'], y = rsf_df['Rank (Hong Kong)'], mode = 'lines+markers',
                         name = 'Global Rank (Hong Kong)', yaxis = 'y2',
                         marker_color = '#ff8000',
                         marker_size = 9))

# update layout to improve readability of data visualization
fig.update_layout(title = 'Press Freedom Index and Ranking 2013-2022<br><sup>A Decline in Press Freedom</sup>',
                  titlefont = dict(size = 28,
                                   family = 'Trajan'),
                  xaxis = dict(title = 'Year', 
                               domain = [0.01, 0.99], 
                               tickmode = 'linear',
                               tickfont = dict(size = 15,
                                               family = 'Trajan'),
                               titlefont = dict(size = 18,
                                                family = 'Trajan')), 
                  yaxis = dict(title = 'Score',
                               tickfont = dict(size = 15,
                                               family = 'Trajan'),
                               titlefont = dict(size = 18,
                                                family = 'Trajan'),
                               position = 0),
                  yaxis2 = dict(title = 'Rank', side = 'right', overlaying = 'y',
                                tickfont = dict(size = 15,
                                                family = 'Trajan'),
                                titlefont = dict(size = 18,
                                                 family = 'Trajan'),
                                position = 1),
                  yaxis_range = [0, 100], 
                  yaxis2_range = [180, 1],
                  yaxis_showgrid = True,
                  yaxis2_showgrid = False, 
                  bargap = 0.15,
                  bargroupgap = 0.08,
                  legend = dict(
                      x = 0.02,
                      y = 0.98,
                      bgcolor = 'rgba(255, 255, 255, 0)',
                      bordercolor = 'rgba(255, 255, 255, 0)',
                      font = dict(size = 15,
                                  family = 'Trajan')))

# source as footnote
note = 'Source:<a href="https://rsf.org/en/index">Reporters Without Borders</a>'

fig.add_annotation(
    showarrow=False,
    text=note,
    font=dict(size=13,
              family = 'Trajan'), 
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.05
    )

py.plot(fig, filename = 'rsf', auto_open = True)

fig.show()


