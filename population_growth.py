#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 17:26:54 2023

@author: jasonlcyy
"""
import pandas as pd
import plotly.express as px
import chart_studio
import chart_studio.plotly as py

# chart studio setup
username = 'Jasonlcyy'
api_key = 'M7tIXqtBJct4PZMO6cQJ'
chart_studio.tools.set_credentials_file(username=username,
                                        api_key=api_key)

# read data
hk_population = pd.read_csv(
    "/Users/jasonlcyy/Desktop/HK Project/Hong Kong Population.csv")

# remove digit separators to prepare for data conversion
hk_population['Population'] = hk_population['Population'].apply(
    lambda x: int(x.replace(',', '')))

# remove percentage unit for data conversion
hk_population['Growth'] = hk_population['Growth'].apply(
    lambda x: float(x.replace('%', '')))

# sort valeus of year from low to high
hk_population = hk_population.sort_values(by='Year', ascending=True)

# line chart
hk_population_fig = px.line(hk_population, x='Year', y='Population')

# update layout for better readability
hk_population_fig.update_layout(title='Hong Kong Population 1950-2022<br><sup>Slightly Decreased since 2021</sup>',
                                titlefont=dict(size=28,
                                               family='Trajan'),
                                xaxis=dict(title='Year',
                                           domain=[0.01, 0.99],
                                           tickfont=dict(size=15,
                                                         family='Trajan'),
                                           titlefont=dict(size=18,
                                                          family='Trajan')),
                                yaxis=dict(title='Population (Millions)',
                                           tickfont=dict(size=15,
                                                         family='Trajan'),
                                           titlefont=dict(size=18,
                                                          family='Trajan'),
                                           position=0,
                                           showexponent='none'))

# add vertical rectangle to highlight the emphasis of data
hk_population_fig.add_vrect(x0=2018, x1=2022,
                            opacity=0.5,
                            fillcolor='LightSalmon',
                            layer='below', line_width = 0)

# source note
hk_population_note = 'Source:<a href="https://www.macrotrends.net/countries/HKG/hong-kong/population">MacroTrends</a>'

hk_population_fig.add_annotation(
    showarrow=False,
    text=hk_population_note,
    font=dict(size=13,
              family='Trajan'),
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.2
)

py.plot(hk_population_fig, filename = "population", auto_open = True)

hk_population_fig.show()

''' hk population yoy '''

hk_population_yoy = px.line(hk_population, x='Year', y='Growth')

hk_population_yoy.update_layout(title='Hong Kong Population Year-on-year Growth 1950-2022<br><sup>Slightly Decreased since 2021</sup>',
                                titlefont=dict(size=28,
                                               family='Trajan'),
                                xaxis=dict(title='Year',
                                           domain=[0.01, 0.99],
                                           tickfont=dict(size=15,
                                                         family='Trajan'),
                                           titlefont=dict(size=18,
                                                          family='Trajan')),
                                yaxis=dict(range=[-5.00, 5.00],
                                           title='Year-on-year Growth (%)',
                                           tickfont=dict(size=15,
                                                         family='Trajan'),
                                           titlefont=dict(size=18,
                                                          family='Trajan'),
                                           tickformat='.2f',
                                           position=0))

# add vertical rectangle to highlight the emphasis of data
hk_population_yoy.add_vrect(
    x0=2013, x1=2022,
    fillcolor='LightSalmon', opacity=0.5,
    layer='below', line_width=0)

hk_population_yoy.add_annotation(
    showarrow=False,
    text=hk_population_note,
    font=dict(size=13,
              family='Trajan'),
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.2
)

py.plot(hk_population_yoy, filename = "population YoY", auto_open = True)

hk_population_yoy.show()