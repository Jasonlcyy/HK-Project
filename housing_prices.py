#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 20:35:35 2022

@author: jasonlcyy
"""

import pandas as pd
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py

# chart studio setup
username = 'Jasonlcyy'
api_key = 'M7tIXqtBJct4PZMO6cQJ'
chart_studio.tools.set_credentials_file(username=username,
                                        api_key=api_key)

# read web scraping data
numbeo_summary = pd.read_csv('/Users/jasonlcyy/Desktop/FINA2390/project3_output.csv')

# rename column of data
numbeo_summary.rename(columns = {'Unnamed: 0': 'City'}, inplace = True)

# only attain valid data
housing_prices = numbeo_summary[['City','Cost of Living - Price per Square Meter to Buy Apartment in City Centre', 
                'Cost of Living - Price per Square Meter to Buy Apartment Outside of Centre']].reset_index(drop = True).dropna()
# convert string data type to double for sorting
housing_prices['Cost of Living - Price per Square Meter to Buy Apartment in City Centre'] = pd.to_numeric(
    housing_prices['Cost of Living - Price per Square Meter to Buy Apartment in City Centre'])

housing_prices['Cost of Living - Price per Square Meter to Buy Apartment Outside of Centre'] = pd.to_numeric(
    housing_prices['Cost of Living - Price per Square Meter to Buy Apartment Outside of Centre'])

# sort values by city centre prices from high to low
housing_prices = housing_prices.sort_values(
    by = 'Cost of Living - Price per Square Meter to Buy Apartment in City Centre', ascending = False)

# list of colors to highlight certain columns in plotly bar charts
housing_colors = ['#6666ff']*20
housing_colors[18] = '#73264d'
outside_colors = ['#75a3a3']*20
outside_colors[18] = '#00264d'

# declare and customise plotly figure
housing_prices_fig = go.Figure()

# add bar chart for city centre housing prices
housing_prices_fig.add_trace(go.Bar(x=housing_prices['Cost of Living - Price per Square Meter to Buy Apartment in City Centre'].iloc[19::-1],
                                 y=housing_prices['City'].iloc[19::-1],
                                 name='Price per Square Meter to Buy Apartment in City Centre',
                                 orientation='h',
                                 marker_color=outside_colors,
                                 offsetgroup=2))

# add bar chart for outside city centre housing prices
housing_prices_fig.add_trace(go.Bar(x=housing_prices['Cost of Living - Price per Square Meter to Buy Apartment Outside of Centre'].iloc[19::-1],
                                 y=housing_prices['City'].iloc[19::-1],
                                 name='Price per Square Meter to Buy Apartment Outside of Centre',
                                 orientation='h',
                                 marker_color=housing_colors,
                                 offsetgroup=1))

# update layout to improve data viz readability
housing_prices_fig.update_layout(title='Housing Prices - Top 20 Cities<br><sup>Ranked 2nd Out of 899 Cities</sup>',
                              titlefont=dict(size=28,
                                             family='Trajan'),
                              xaxis=dict(title='US Dollars (Thousands)',
                                         domain=[0.01, 0.99],
                                         tickfont=dict(size=15,
                                                       family='Trajan'),
                                         titlefont=dict(size=18,
                                                        family='Trajan'),
                                         showexponent='none',),
                              yaxis=dict(title='City',
                                         position=0,
                                         tickfont=dict(size=15,
                                                       family='Trajan'),
                                         titlefont=dict(size=18,
                                                        family='Trajan')),
                              legend = dict(
                                  x = 0.7, y = 0.9,
                                  bgcolor = 'rgba(255, 255, 255, 0)',
                                  bordercolor = 'rgba(255, 255, 255, 0)',
                                  font = dict(size = 15,
                                              family = 'Trajan'),
                                  traceorder = 'reversed'),
                              barmode='group',
                              bargap=0.15,
                              bargroupgap=0.08)

# source as footnote
housing_prices_note = 'Source:<a href="https://www.numbeo.com/cost-of-living/">Numbeo</a>'

# add footnote
housing_prices_fig.add_annotation(
    showarrow=False,
    text=housing_prices_note,
    font=dict(size=13,
              family='Trajan'),
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.2
)

py.plot(housing_prices_fig, filename = "housing prices", auto_open=True)

housing_prices_fig.show()


