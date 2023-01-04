#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 21:28:05 2022

@author: jasonlcyy
"""
from selenium import webdriver
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py

# chart studio setup
username = 'Jasonlcyy'
api_key = 'M7tIXqtBJct4PZMO6cQJ'
chart_studio.tools.set_credentials_file(username=username,
                                        api_key=api_key)

# chromedriver path
driver_path = "/Users/jasonlcyy/Downloads/chromedriver"
browser = webdriver.Chrome(executable_path = driver_path)

link = "https://www.numbeo.com/property-investment/rankings.jsp?title={}"

yearly_data = []

for i in range(2009, 2023):
    # empty lists to store cities and their respective ratios
    cities = []
    P2I = []
    browser.get(link.format(str(i)))
    for row in range(1, 500):
        try:
            # scrap city and ratio till all data is scraped
            temp = browser.find_element('xpath', '//*[@id="t2"]/tbody/tr[{}]/td[2]'.format(str(row)))
            cities.append(temp.text)
            temp = browser.find_element('xpath', '//*[@id="t2"]/tbody/tr[{}]/td[3]'.format(str(row)))
            P2I.append(float(temp.text))
        except:
            break
        # append city and ratio pair to the master data list
    yearly_data.append([cities, P2I])

browser.quit()

yearly_dataframe = []

for i in yearly_data:
    # append the dataframe with city and ratio data to list
    yearly_dataframe.append(pd.DataFrame(list(zip(i[0], i[1])), columns = ['City', 'Price-to-Income Ratio']))

year_rank = []
year_P2I = []
global_mean = []

# skip first two years of data without Hong Kong data
for year in range(2, len(yearly_dataframe)):
    # locate the rank, ratio and global average of different years
    year_P2I.append(yearly_dataframe[year][yearly_dataframe[year]['City'] == 'Hong Kong, Hong Kong (China)']['Price-to-Income Ratio'].values[0])
    global_mean.append(yearly_dataframe[year]['Price-to-Income Ratio'].mean())
    year_rank.append(yearly_dataframe[year].index[yearly_dataframe[year]['City'] == 'Hong Kong, Hong Kong (China)'][0]+1)

# year array for x axis
P2I_years = np.arange(2011, 2023)

# construct dataframe for plotly output
P2I_output = pd.DataFrame({'Year': P2I_years, 'Price-to-Income Ratio': year_P2I, 'Rank': year_rank, 'Global mean': global_mean})

''' read csv '''
# P2I_output = pd.read_csv('/Users/jasonlcyy/Desktop/HK Project/P2I_rank.csv')

# declare plotly figure
P2I_fig = go.Figure()

# add ratio as bar chart
P2I_fig.add_trace(go.Bar(x = P2I_output['Year'], y = P2I_output['Price-to-Income Ratio'],
                         name = 'Hong Kong', yaxis = 'y',
                         marker_color = '#000066'))

# add global average as bar chart
P2I_fig.add_trace(go.Bar(x = P2I_output['Year'], y = P2I_output['Global mean'],
                         name = 'Global Mean', yaxis = 'y',
                         marker_color = '#b3c6ff'))

# add rank as line chart
P2I_fig.add_trace(go.Scatter(x = P2I_output['Year'], y = P2I_output['Rank'],
                             mode = 'lines+markers',
                             name = 'Global Rank (Hong Kong)', yaxis = 'y2',
                             marker_color = '#ff8000',
                             marker_size = 9))

# update layout for better readability
P2I_fig.update_layout(title = 'Price-to-Income Ratio 2011-2022<br><sup>Skyhigh Property Prices</sup>',
                      titlefont = dict(size = 28,
                                       family = 'Trajan'),
                      xaxis = dict(title = 'Year',
                                   tickmode = 'linear',
                                   tickfont = dict(size = 15,
                                                   family = 'Trajan'),
                                   titlefont = dict(size = 18,
                                                    family = 'Trajan'),
                                   domain = [0.01, 0.99]),
                      yaxis = dict(title = 'Price-to-Income Ratio',
                                   tickfont = dict(size = 15,
                                                   family = 'Trajan'),
                                   titlefont = dict(size = 18,
                                                    family = 'Trajan'),
                                   position = 0),
                      yaxis2 = dict(title = 'Rank',
                                    overlaying = 'y', side = 'right',
                                    showgrid = False,
                                    tickfont = dict(size = 15,
                                                    family = 'Trajan'),
                                    titlefont = dict(size = 18,
                                                     family = 'Trajan'),
                                    position = 1,
                                    range = [100, 0]),
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
P2I_note = 'Source:<a href="https://www.numbeo.com/property-investment/rankings.jsp">Numbeo</a>'

P2I_fig.add_annotation(
    showarrow=False,
    text=P2I_note,
    font=dict(size=13,
              family = 'Trajan'), 
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.2
    )

py.plot(P2I_fig, filename = "Price to Income", auto_open = True)

P2I_fig.show()
