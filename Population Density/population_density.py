# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 13:49:24 2022

@author: A0835647
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
df = pd.read_csv('/Users/jasonlcyy/Desktop/HK Project/Population Density.csv')

# replace thousand separators to prepare for data conversion
df['Population Estimate'] = df['Population Estimate'].apply(
    lambda x: x.replace(',', ''))
df['Built-up Land Area (Miles)'] = df['Built-up Land Area (Miles)'].apply(
    lambda x: x.replace(',', ''))
df['Built-up Land Area (Kilometers)'] = df['Built-up Land Area (Kilometers)'].apply(
    lambda x: x.replace(',', ''))
df['Urban Population Density (Per Square Mile)'] = df['Urban Population Density (Per Square Mile)'].apply(
    lambda x: x.replace(',', ''))
df['Urban Population Density (Per Square Kilometer)'] = df['Urban Population Density (Per Square Kilometer)'].apply(
    lambda x: x.replace(',', ''))

# convert all column to double
df[['Population Estimate',
    'Built-up Land Area (Miles)', 'Built-up Land Area (Kilometers)',
    'Urban Population Density (Per Square Mile)',
    'Urban Population Density (Per Square Kilometer)']] = df[['Population Estimate',
                                                              'Built-up Land Area (Miles)', 'Built-up Land Area (Kilometers)',
                                                              'Urban Population Density (Per Square Mile)',
                                                              'Urban Population Density (Per Square Kilometer)']].apply(pd.to_numeric)

# sort values by population density from high to low                                                              
population_density = df[['Country', 'City', 'Population Estimate',
                         'Built-up Land Area (Miles)', 'Built-up Land Area (Kilometers)',
                         'Urban Population Density (Per Square Mile)',
                         'Urban Population Density (Per Square Kilometer)']].sort_values(by='Urban Population Density (Per Square Kilometer)', ascending=False).reset_index(drop=True)

# color array to specify colors of bars
pop_colors = ['#6666ff']*20
pop_colors[11] = '#73264d'

# declare plotly figure
pop_density_fig = go.Figure()

# add horizontal bar chart for land area of top 20 cities in terms of population density
pop_density_fig.add_trace(go.Bar(x=population_density['Built-up Land Area (Kilometers)'].iloc[19::-1],
                                 y=population_density['City'].iloc[19::-1],
                                 name='Land Area',
                                 orientation='h',
                                 marker_color='#75a3a3',
                                 xaxis='x2',
                                 offsetgroup=2))

# add horizontal bar chart for population density of top 20 cities in terms of population density
pop_density_fig.add_trace(go.Bar(x=population_density['Urban Population Density (Per Square Kilometer)'].iloc[19::-1],
                                 y=population_density['City'].iloc[19::-1],
                                 name='Population Density',
                                 orientation='h',
                                 marker_color=pop_colors,
                                 xaxis='x',
                                 offsetgroup=1))

# update layout to improve readability
pop_density_fig.update_layout(title='Urban Population Density - Top 20 Cities<br><sup>Ranked 9th Out of 954 Cities</sup>',
                              titlefont=dict(size=28,
                                             family='Trajan'),
                              xaxis=dict(title='Urban Population Density (Thousands Per Square Kilometer)',
                                         domain=[0.01, 0.99],
                                         tickfont=dict(size=15,
                                                       family='Trajan'),
                                         titlefont=dict(size=18,
                                                        family='Trajan'),
                                         showexponent='none',
                                         side='top',
                                         overlaying='x2'),
                              xaxis2=dict(title='Built-up Land Area (Square Kilometer)',
                                          # overlaying = 'x',
                                          domain=[0.01, 0.99],
                                          side='bottom',
                                          tickfont=dict(size=15,
                                                        family='Trajan'),
                                          titlefont=dict(size=18,
                                                         family='Trajan'),
                                          showexponent='none',
                                          showgrid=False),
                              yaxis=dict(title='City',
                                         position=0,
                                         tickfont=dict(size=15,
                                                       family='Trajan'),
                                         titlefont=dict(size=18,
                                                        family='Trajan')),
                              legend = dict(
                                  x = 0.88, y = 0.9,
                                  bgcolor = 'rgba(255, 255, 255, 0)',
                                  bordercolor = 'rgba(255, 255, 255, 0)',
                                  font = dict(size = 15,
                                              family = 'Trajan'),
                                  traceorder = 'reversed'),
                              barmode='group',
                              bargap=0.15,
                              bargroupgap=0.08)

# source note
pop_density_note = 'Source:<a href="http://www.demographia.com/">Demographia</a>'

pop_density_fig.add_annotation(
    showarrow=False,
    text=pop_density_note,
    font=dict(size=13,
              family='Trajan'),
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.2
)

py.plot(pop_density_fig, filename = "population density", auto_open = True)

pop_density_fig.show()