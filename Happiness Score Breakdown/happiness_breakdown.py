#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 17:25:56 2023

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

# read data
happiness_breakdown = pd.read_csv(
    "/Users/jasonlcyy/Desktop/HK Project/Happiness Breakdown.csv")

# group by year to attain yearly global average of indices as reference plot
mean_freedom_confidence = happiness_breakdown[[
    'year', 'Freedom to make life choices', 'Confidence in national government']].groupby(by='year').mean()

# hong kong index
hk_freedom_confidence = happiness_breakdown[happiness_breakdown['Country name'] == 'Hong Kong S.A.R. of China'][[
    'Country name', 'year', 'Freedom to make life choices', 'Confidence in national government']]

# left join hk data and global average on year
combine = pd.merge(mean_freedom_confidence,
                   hk_freedom_confidence, how='left', on='year')

# drop country name column
combine.drop('Country name', axis=1, inplace=True)

# rename columns for better accessibility
combine.rename({'Freedom to make life choices_x': 'Freedom to make life choices WW',
                'Confidence in national government_x': 'Confidence in national government WW',
                'Freedom to make life choices_y': 'Freedom to make life choices HK',
                'Confidence in national government_y': 'Confidence in national government HK'}, axis=1, inplace=True)

# remove the first datapoint, which is missing for Hong Kong
combine = combine.iloc[1:]

# declare plotly figure
freedom_fig = go.Figure()

# add hk indices as line chart and indicate legend group for grouping 
freedom_fig.add_trace(go.Scatter(x=combine['year'], y=combine['Freedom to make life choices HK'],
                                 mode='lines+markers',
                                 name='Hong Kong',
                                 legendgroup='Freedom to Make Life Choices',
                                 legendgrouptitle_text='Freedom to Make Life Choices',
                                 marker_color='#003d99'))
# add worldwide average indices as line chart and indicate legend group for grouping
freedom_fig.add_trace(go.Scatter(x=combine['year'], y=combine['Freedom to make life choices WW'],
                                 mode='lines+markers',
                                 name='Global average',
                                 legendgroup='Freedom to Make Life Choices',
                                 marker_color='#66a3ff'))

freedom_fig.add_trace(go.Scatter(x=combine['year'], y=combine['Confidence in national government HK'],
                                 mode='lines+markers',
                                 name='Hong Kong',
                                 legendgroup='Confidence in national government',
                                 legendgrouptitle_text='Confidence in national government',
                                 marker_color='#990000'))

freedom_fig.add_trace(go.Scatter(x=combine['year'], y=combine['Confidence in national government WW'],
                                 mode='lines+markers',
                                 name='Global average',
                                 legendgroup='Confidence in national government',
                                 marker_color='#ff6666'))

# connect gaps of missing data points for readability
freedom_fig.update_traces(connectgaps=True)

# update layout for better readability
freedom_fig.update_layout(font_family = 'Trajan',
                          font_size = 15,
                          title='Political-related Indices Breakdown From World Happiness Index<br><sup>Decline Due to Political Events</sup>',
                          titlefont=dict(size=28,
                                         family='Trajan'),
                          xaxis=dict(title='Year',
                                     domain=[0.01, 1],
                                     tickmode='linear',
                                     tickfont=dict(size=15,
                                                   family='Trajan'),
                                     titlefont=dict(size=18,
                                                    family='Trajan'),
                                     showgrid=False),
                          yaxis=dict(title='Index',
                                     tickfont=dict(size=15,
                                                   family='Trajan'),
                                     titlefont=dict(size=18,
                                                    family='Trajan'),
                                     tickformat='.2f',
                                     position=0,
                                     showgrid=False),
                          legend=dict(x=0.86, y=0.98,
                                      bgcolor='rgba(255, 255, 255, 0)',
                                      font = dict(size = 15,
                                                  family = 'Trajan')))

# add vertical rectangles to highlight emphasis points
freedom_fig.add_vrect(
    x0=2011.5, x1=2014.5,
    fillcolor='LightSalmon', opacity=0.5,
    layer='below', line_width=0)

freedom_fig.add_vrect(
    x0=2016.5, x1=2019.5,
    fillcolor='LightSalmon', opacity=0.5,
    layer='below', line_width=0)

# source footnote
freedom_note = 'Source:<a href="https://worldhappiness.report/">World Happiness Report</a>'

freedom_fig.add_annotation(
    showarrow=False,
    text=freedom_note,
    font=dict(size=13,
              family='Trajan'),
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.2
)

py.plot(freedom_fig, filename = 'freedom', auto_open = True)

freedom_fig.show()